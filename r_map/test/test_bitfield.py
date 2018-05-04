from random import randint
def test_bitfield(data):
    reg = data.spi.cfg0

    f = reg.bf0.bf

    reg.value = 0xFFFFFFFF

    print(f"Reg value now: {reg.value}")

    assert f.value == (1<<f.width)-1

    expected_reg_value = 0

    for f in reg:
        n = randint(0, 0xFFFFFFFF)

        f.value = n

        expected_reg_value |= f.value

    assert expected_reg_value == reg.value

