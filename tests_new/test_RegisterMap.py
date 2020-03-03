import r_map
from r_map.elaborate_tree import elaborate_nodes, convert_to_fixed_node

def test_elaborated_register_map(reg):
    reg_map = r_map.RegisterMap(name='reg_map', local_address=0x100)
    reg_map._add(reg._copy())

    r = reg_map[reg.name]
    assert r.parent is reg_map
    elaborate_nodes(reg_map)
    convert_to_fixed_node(reg_map)

    r = reg_map[reg.name]
    print(f"reg_map.address: {reg_map.address:#010x}")
    print(f"r address: {r.address:#010x}")
    assert r.address == 0x100



def test_arrayed_register_map(reg):
    root = r_map.AddressedNode(name='root', local_address=0)
    arrayed_reg = r_map.ArrayedNode(
            name='TX_FIFO[m]',
            start_index=0,
            incr_index=1,
            array_letter='m',
            descr='TX FIFO register [mm]',
            end_index=4,
            increment=0x4,
            base_val=0)
    root._add(arrayed_reg)


    arrayed_reg.base_node=reg._copy(local_address=0x10)
    assert arrayed_reg[1].address == 4

    elaborate_nodes(root)
    convert_to_fixed_node(root)
    print(list(map(str, root)))

    assert root.TX_FIFO2.address == 8
    assert 'TX_FIFO[m]' not in root

    prim = r_map.dump(root)
    root2 = r_map.load(prim)
    assert root2.TX_FIFO2.address == 8








