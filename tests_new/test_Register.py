import random
from operator import or_
from functools import reduce, partial
from pprint import PrettyPrinter
import r_map

rand_int = partial(random.randint, 0, 0xFFFFFFFF)

def test_validate_reg(reg):
    errors = list(reg.validate())
    assert len(errors) == 0

def test_reg_apply_value(reg):
    "Test that the value's new value is set according to its children's widths"

    new_val = rand_int()
    new_val_mask = (1 << (reg.bf1_ref.slice_width+reg.bf2_ref.slice_width)) - 1
    reg.value = new_val
    exp = new_val & new_val_mask
    assert reg.value == exp, f"Expected reg.value=={exp:#010x}, got:{reg.value:#010x}"

def test_reg_reset(reg):
    """Ensure that a register's reset value matches the sum of its child
    BitFieldRef's reset values"""
    new_val = random.randint(0, 0xFFFFFFFFFF)
    reg.value = new_val
    reg.reset()
    expected_reset_val = reduce(or_, (r.value for r in reg))
    assert reg.value == expected_reset_val


def test_reg_copy(reg):
    root = r_map.Node(name='root')
    reg1 = reg

    print(f"reg1.bf1_ref.bf1: {reg1.bf1_ref.bf1!r}")
    reg2 = reg1._copy(name='reg2')
    root._add(reg2)
    print("Children in reg2:")
    for c in reg2:
        print(repr(c))

    assert reg1.bf1_ref is not reg2.bf1_ref
    assert reg1.bf1_ref.bf1 is not reg2.bf1_ref.bf1

def test_reg_alias(reg):
    """test that when a register is made to be an alias of another, it  gets
    deep copied until the level of bitfieldref."""
    root = r_map.Node(name='root')
    reg1 = reg

    print(f"reg1.bf1_ref.bf1: {reg1.bf1_ref.bf1!r}")
    reg2 = reg1._copy(name='reg2', new_instance=True, new_alias=True)
    root._add(reg2)
    print("Children in reg2:")
    for c in reg2:
        print(repr(c))

    assert reg1.bf1_ref is not reg2.bf1_ref
    assert reg1.bf1_ref.bf1 is reg2.bf1_ref.bf1

def test_install_bitfield(reg, bf):
    """Check that children of registers need to be of type BitFieldRef and not
    BitField"""
    reg._add(bf)
    assert bf.parent == reg
    errors = list(reg.validate())
    assert len(errors) == 1
    assert 'is not of type' in errors[0].error

def test_validate_no_bitrefs_present():
    """Check that validation flags an error if no bitfieldrefs are present"""
    reg = r_map.Register(name='some_reg', local_address=0)
    errors = list(reg.validate())
    for error in errors:
        print(str(error))
    assert len(errors) == 1
    assert 'No bitfieldrefs present' in errors[0].error

def test_iterate_over_reg(reg):
    bfs = list(reg)
    assert len(bfs) == 2

def test_serialize_reg(reg):
    root = r_map.Node(name='root')
    reg_copy = reg._copy(name=reg.name+'_copy', new_instance=True, new_alias=True)
    assert reg_copy.bf1_ref.bf1 is reg.bf1_ref.bf1
    assert reg.bf1_ref.reg_offset == 0
    root._add(reg)
    root._add(reg_copy)
    primitive = r_map.dump(root)
    assert reg.bf1_ref.reg_offset == 0
    print(primitive)
    root2 = r_map.load(primitive)
    assert root2.reg1.bf1_ref.bf1 is root2.reg1_copy.bf1_ref.bf1
    assert root2.reg1.bf2_ref.bf2 is root2.reg1_copy.bf2_ref.bf2
    assert root2.reg1.bf2_ref is not root2.reg1_copy.bf2_ref
    assert root2.reg1.bf2_ref.uuid != root2.reg1_copy.bf2_ref.uuid

def test_deserialize_reg_custom(reg):
    root = r_map.Node(name='root')
    root._add(reg)
    prim = r_map.dump(root)

    class RegisterCustom(r_map.Register):
        pass

    root_custom = r_map.load(prim, {'Register':RegisterCustom})
    root2 = r_map.load(prim)

    assert isinstance(root_custom.reg1, RegisterCustom)
    assert isinstance(root2.reg1, r_map.Register)
    assert not isinstance(root2.reg1, RegisterCustom)



def test_arrayed_register(reg):
    arrayed_reg = r_map.ArrayedNode(
            name='TX_FIFO[nn]_[n]',
            start_index=0,
            incr_index=4,
            descr='TX FIFO register [nn]',
            end_index=20*4,
            increment=0x4,
            base_val=0x100)
    arrayed_reg.base_node=reg

    r = arrayed_reg[4]
    assert r.name == 'TX_FIFO04_4'
    assert r.address == 0x104
    r = arrayed_reg['TX_FIFO08_8']
    assert r.name == 'TX_FIFO08_8'
    assert r.address == 0x108

    assert r.descr == 'TX FIFO register 08'

def test_arrayed_ref_register(reg):
    root = r_map.Node(name='root')

    reg = r_map.Register(name='a_reg', local_address=0)
    bf_ref = r_map.BitFieldRef(name='a_bf_ref', reg_offset=0)
    reg._add(bf_ref)
    bf = r_map.BitField(name='a_bf', width=8)
    bf_ref._add(bf)

    arrayed_reg = r_map.ArrayedNode(
            name='TX_FIFO[nn]_[n]',
            start_index=0,
            incr_index=4,
            descr='TX FIFO register [nn]',
            end_index=20*4,
            increment=0x4,
            base_val=0x100,
            base_node=reg)
    root._add(arrayed_reg)

    arrayed_reg_2 = arrayed_reg._copy(new_instance=True, new_alias=True, name='TX_FIFO2[nn]_[n]')

    r1 = arrayed_reg[4]
    r1.value = 0x12
    assert r1.value == 0x12
    r2 = arrayed_reg['TX_FIFO08_8']
    r2.value = 0x23
    assert r1.value == 0x12
    assert r2.value == 0x23

    r1_copy = arrayed_reg_2[4]
    assert r1_copy.value == 0x12
    r2_copy = arrayed_reg_2[8]
    assert r2_copy.value == 0x23


def test_arrayed_ref_register_serialized(reg):
    root = r_map.Node(name='root')

    reg = r_map.Register(name='a_reg', local_address=0)
    bf_ref = r_map.BitFieldRef(name='a_bf_ref', reg_offset=0)
    reg._add(bf_ref)
    bf = r_map.BitField(name='a_bf', width=8)
    bf_ref._add(bf)

    arrayed_reg = r_map.ArrayedNode(
            name='TX_FIFO[nn]_[n]',
            start_index=0,
            incr_index=4,
            descr='TX FIFO register [nn]',
            end_index=20*4,
            increment=0x4,
            base_val=0x100,
            base_node=reg)
    root._add(arrayed_reg)

    arrayed_reg_2 = arrayed_reg._copy(new_instance=True, new_alias=True,
                                      name='TX_FIFO2[nn]_[n]')
    root._add(arrayed_reg_2)

    r1 = arrayed_reg[4]
    r1.value = 0x12
    assert r1.value == 0x12
    r2 = arrayed_reg['TX_FIFO08_8']
    r2.value = 0x23
    assert r1.value == 0x12
    assert r2.value == 0x23

    r1_copy = arrayed_reg_2[4]
    assert r1_copy is root['TX_FIFO2'][4]
    assert r1_copy.value == 0x12
    r2_copy = arrayed_reg_2[8]
    assert r2_copy.value == 0x23


    primitive = r_map.dump(root)
    #PrettyPrinter(indent=4).pprint(primitive)
    root2 = r_map.load(primitive)

    arrayed_reg_copy = root2['TX_FIFO']
    arrayed_reg_2_copy = root2['TX_FIFO2']

    r1 = arrayed_reg_copy[4]
    r1.value = 0x12
    assert r1.value == 0x12
    r2 = arrayed_reg_copy['TX_FIFO08_8']
    r2.value = 0x23
    assert r1.value == 0x12
    assert r2.value == 0x23

    #test reflected methods
    assert r1 == 0x12
    assert 0x12 == r1
    assert r1 >= 0x12
    assert r1 >= 0x11
    assert 0x11 <= r1
    assert 0x12 <= r1
    assert 0x13 > r1
    assert r1 < 0x13
    assert r1 < r2
    assert r1 <= r2
    assert r2 > r1
    assert r2 >= r1


    r1_copy = arrayed_reg_2_copy[4]
    assert r1_copy.value == 0x12
    r2_copy = arrayed_reg_2_copy[8]
    assert r2_copy.value == 0x23

def test_reg_copy_serialized(reg):
    reg_copy = reg._copy()

    primitive = r_map.dump(reg_copy)
    reg_copy_2 = r_map.load(primitive)
    assert len(reg_copy_2) == len(reg_copy)

    errors = list(reg_copy_2.validate())
    assert len(errors) == 0

def test_nested_arrayed_register(reg):
    arrayed_map = r_map.ArrayedNode(
            name='TX_MAP[n]',
            start_index=0,
            incr_index=4,
            descr='TX Register Map [nn]',
            end_index=8,
            increment=0x10000,
            base_val=0x10000)

    arrayed_reg = r_map.ArrayedNode(
            name='TX_FIFO[n]',
            start_index=0,
            incr_index=4,
            descr='TX FIFO register [nn]',
            end_index=20*4,
            increment=0x4,
            base_val=0x100)

    arrayed_reg.base_node=reg
    arrayed_map.base_node = arrayed_reg

    for map_ in arrayed_map:
        for reg in map_:
            print(f'{reg} -> parent: {reg.parent}')

def test_write(reg):
    written = None
    def writer(address, value:int):
        nonlocal written
        written = value

    reg._reg_write_func = writer

    reg.write(0x12345)

    assert written == 0x12345

def test_write_ex(reg):
    written = None
    def writer(reg, value:int):
        nonlocal written
        written = value

    reg._reg_write_ex_func = writer

    reg.write(0x12345)

    assert written == 0x12345

def test_read_ex(reg):
    read_back = None
    def reader(address):
        nonlocal read_back
        read_back = 0x12346
        return read_back

    reg._reg_read_func = reader

    assert 0x12346 == reg.read()


def test_read_ex(reg):
    read_back = None
    def reader(reg):
        nonlocal read_back
        address = reg.address
        read_back = 0x12346
        return read_back

    reg._reg_read_ex_func = reader

    assert 0x12346 == reg.read()

def test_bitfield_shorthand(reg):
    assert reg.bf1_ref == reg.bf1_ref.bf.reset_val
    assert reg.bf1_ref >= reg.bf1_ref.bf.reset_val
    assert reg.bf1_ref > reg.bf1_ref.bf.reset_val - 1
    assert reg.bf1_ref.bf.reset_val >= reg.bf1_ref
    assert reg.bf1_ref.bf.reset_val - 1 <= reg.bf1_ref
    assert reg.bf1_ref.bf.reset_val - 1 <= reg.bf1_ref
    reg.bf2_ref = reg.bf2_ref.bf.reset_val + 1
    assert reg.bf2_ref == reg.bf2_ref.bf.reset_val + 1

def test_deep_copy_reg(reg):
    bf1_ref2 = reg.bf1_ref._copy(name='bf1_ref2')
    assert bf1_ref2.bf is not reg.bf1_ref.bf

def test_deep_copy_reg2(reg):
    bf1_ref2 = reg.bf1_ref._copy(name='bf1_ref2', _deep_copy=False)
    assert bf1_ref2.bf is reg.bf1_ref.bf

def test_deep_copy_reg3(reg):
    bf1_ref2 = reg.bf1_ref._copy(name='bf1_ref2', new_alias=True)
    assert bf1_ref2.bf is reg.bf1_ref.bf


