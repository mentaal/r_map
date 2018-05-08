from r_map.RMapJSON import to_json, from_json
def test_encode_to_json(basic_data):

    for obj in basic_data._walk(top_down=True, levels=-1):
        print(obj)

    json_data = to_json(basic_data, indent=4)
    print(json_data)



def test_decode_from_json(basic_data):
    json_data = to_json(basic_data)
    print("Json data to decode: ", json_data)
    root = from_json(json_data)

    #do this twice to ensure that closures working as expected
    root = from_json(json_data)

    #ensure that bitfields are the same
    assert root.r_map1.reg1.bf1_ref.bf is root.r_map1.reg2.bf2_ref.bf


    for obj in root._walk(top_down=True, levels=-1):
        print(obj)

    bf = root.r_map1.reg1.bf1_ref.bf

    assert len(bf.references) == 2

    #ensure that references are created properly during deserialization process
    assert bf.references == set([root.r_map1.reg1.bf1_ref, root.r_map1.reg2.bf2_ref])