import json
import r_map

def test_encode_to_json(basic_data):
    for obj in basic_data._walk(top_down=True, levels=-1):
        print(obj)
    prim = r_map.dump(basic_data)
    json_data = json.dumps(prim, indent=4)
    print(json_data)

def test_decode_from_json(basic_data):
    prim = r_map.dump(basic_data)
    json_data = json.dumps(prim, indent=4)
    print(json_data)
    prim = json.loads(json_data)
    root = r_map.load(prim)

    #ensure that bitfields are the same
    assert root.r_map1.reg1.bf1_ref.bf is root.r_map1.reg2.bf2_ref.bf

    for obj in root._walk(top_down=True, levels=-1):
        print(obj)

    bf = root.r_map1.reg1.bf1_ref.bf

    assert len(bf._references) == 2

    #ensure that references are created properly during deserialization process
    assert bf._references == set([root.r_map1.reg1.bf1_ref, root.r_map1.reg2.bf2_ref])


def test_2nd_pass_decode():
    """For a second pass through json data as part of the decoding process"""
    json_data = """
        {
            "name": "root",
            "uuid": "ba328615654f4534a06119fe9bac4130",
            "type": "Node",
            "children": [
                {
                    "descr": "An example register map containing registers",
                    "name": "r_map1",
                    "uuid": "0e493383a1ce45178c5430ea1fe94f81",
                    "local_address": 268435456,
                    "type": "RegisterMap",
                    "children": [
                        {
                            "width": 32,
                            "local_address": 4,
                            "name": "reg2",
                            "uuid": "1495a613e9f34613a7be0c6e2523e691",
                            "type": "Register",
                            "_ref": "d9ca3c5f53f0480d833c2d0d8217d8f7",
                            "_alias": true
                        },
                        {
                            "width": 32,
                            "local_address": 0,
                            "name": "reg1",
                            "uuid": "d9ca3c5f53f0480d833c2d0d8217d8f7",
                            "type": "Register",
                            "children": [
                                {
                                    "slice_width": 6,
                                    "field_offset": 7,
                                    "name": "bf1_ref",
                                    "uuid": "d0d5702adec14404b835742de1b04e67",
                                    "reg_offset": 8,
                                    "type": "BitFieldRef",
                                    "children": [
                                        {
                                            "width": 20,
                                            "doc": "Some documentation to describe the bitfield",
                                            "access": "RW",
                                            "reset_val": 74565,
                                            "name": "bf1",
                                            "uuid": "995d09202644470ba4060f3048ed9272",
                                            "type": "BitField"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }"""

    primitive = json.loads(json_data)
    root = r_map.load(primitive)
    assert root.r_map1.reg1.bf1_ref.bf1 is root.r_map1.reg2.bf1_ref.bf1

