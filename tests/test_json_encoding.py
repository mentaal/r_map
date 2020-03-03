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

