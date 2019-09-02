import r_map

def test_io_block(data):
    first_r_map = next(iter(data))
    assert isinstance(first_r_map, r_map.RegisterMap)
    first_r_map.write()
    first_r_map.read()
    print(first_r_map)
    for r in first_r_map:
        print(r)

def test_io_reg(data):
    first_r_map = next(iter(data))
    first_reg = next(iter(first_r_map))
    first_reg.write(0x1000)
    print(f"Reg now: {first_reg}")
    first_reg.read()
