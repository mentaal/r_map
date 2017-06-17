"""Plugin to register the elements that are actually utilized throughout an
applications's execution. The idea is to register the elements that are actually
utilized and then save these into a separate database which can be used within a
release version of said application - thereby removing any unused elements. The
intention is to create a much smaller database for a release application. 

Utilized elements could be accumulated through the use of unit tests or a subset
of them at least"""

class UsageRegistry():
    def __init__(self):
        self.registry = set()

    def add_registry(self, cls):
        cls.__getattribute__ = type(self).use_registry

    def use_registry(self, key):
        item = object.__getattribute__(self, key)
        nb_attrs = object.__getattribute__(self, '_nb_attrs')
        if key in nb_attrs:
            self.registry.add(self)
        return item

    def complete_tree(self):
        #use a shallow copy of registry as modifying a set whilst iterating over
        #it is not allowed
        for elem in self.registry.copy():
            #traverse each elem up towards the root
            p_elem = elem.parent
            while True:
                if p_elem:
                    self.registry.add(p_elem)
                    p_elem = p_elem.parent
                else:
                    break

    def _serialize(self):
        for item in self.registry:
            yield item._serialize(recurse=False)




