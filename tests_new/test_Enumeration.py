import json
import r_map
from r_map import to_json, from_json


def test_enumeration_inst():
    enum1 = r_map.Enumeration(name='enum1', value=1)
    enum2 = r_map.Enumeration(name='enum2', value=2)
    enum3 = r_map.Enumeration(name='enum3', value=1)

    assert enum1 != enum2
    assert enum1 == enum3
    assert enum1 < enum2
    assert enum1 < 2
    assert enum2 >= enum1
    assert enum2 >= 1
    assert enum2 > enum1
    assert enum1 != 'enum1'

def test_enumeration_negative_validation_error():
    enum1 = r_map.Enumeration(name='enum1', value=-1)
    errors = list(enum1.validate())
    assert len(errors) == 1

def test_enumeration_no_name():
    enum1 = r_map.Enumeration(name='', value=-1)
    errors = list(enum1.validate())
    assert len(errors) == 2

def test_enumeration_to_json():
    "Only test the encoding to json in this test"
    enum1 = r_map.Enumeration(name='enum1', value=-1)
    json_str = to_json(enum1)
    primitive_enum = json.loads(json_str)

    assert primitive_enum['uuid'] == enum1.uuid, 'uuid not encoded correctly'
    for key in enum1._nb_attrs:
        val, encoded_val = getattr(enum1, key), primitive_enum.get(key)
        assert val == encoded_val

def test_enumeration_copy_to_json():
    "test a deepcopy of an enumeration to json"
    root = r_map.Node(name='root')
    enum1 = r_map.Enumeration(name='enum1', parent=root, value=1)
    enum2 = enum1._copy(parent=root, name='enum2', alias=False, deep_copy=True)
    for e in enum1,enum2:
        print(repr(e))
    assert enum1 is not enum2
    assert enum2 in root
    assert enum1 in root
    assert len(root) == 2

    primitive_str = to_json(root)

    print(f"encoded enumerations: {primitive_str}")

def test_dump_enumeration():
    "test turning a tree of nodes into a tree of dicts"
    root = r_map.Node(name='root')
    enum1 = r_map.Enumeration(name='enum1', parent=root, value=1)
    enum2 = enum1._copy(parent=root, name='enum2', alias=False, deep_copy=True)
    for e in enum1,enum2:
        print(repr(e))
    assert enum1 is not enum2
    assert enum2 in root
    assert enum1 in root
    assert len(root) == 2

    primitives = root.dump()

    print(f"encoded enumerations: {primitives}")






