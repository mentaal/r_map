from random import randint
def test_bitfield(data):
    reg = data.spi.cfg0

    f = reg.bf0

    reg.value = 0xFFFFFFFF

    assert f.value == (1<<f.width)-1

    expected_reg_value = 0

    for f in reg:
        n = randint(0, 0xFFFFFFFF)

        f.value = n

        #field_contribution = (((1<<f.width)-1)<<f.position) & n
        field_contribution = (n & ((1<<f.width)-1)) << f.position
        expected_reg_value |= field_contribution

    assert expected_reg_value == reg.value

