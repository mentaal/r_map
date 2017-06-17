from r_map.UsageRegistry import UsageRegistry
from r_map.Node import Node

def test_UsageRegistry(data):
    registry = UsageRegistry()
    registry.add_registry(Node)

    field = data.spi.cfg0.bf0
    print(type(field))
    print(field.name)

    print(registry)

