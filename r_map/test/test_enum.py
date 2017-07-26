def test_enum(data):
    field = data.spi.cfg0.bf0
    print(field.annotation)

    field.value = field.spi_disabled

    assert field.annotation == 'spi_disabled'

    enum = field.spi_enabled

    field.value = enum

    assert field.annotation == 'spi_enabled'


