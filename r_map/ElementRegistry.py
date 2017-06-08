"""Plugin to register the elements that are actually utilized throughout an
applications's execution. The idea is to register the elements that are actually
utilized and then save these into a separate database which can be used within a
release version of said application - thereby removing any unused elements. The
intention is to create a much smaller database for a release application. 

Utilized elements could be accumulated through the use of unit tests or a subset
of them at least"""


from r_map.Node import Node

registry = set()

def registry_use(self, key):
    item = object.__getattribute__(self, key)
    nb_attrs = object.__getattribute__(self, '_nb_attrs')
    if key in nb_attrs:
        registry.add(self)
    return item

def add_registry():
    Node.__getattribute__ = registry_use

