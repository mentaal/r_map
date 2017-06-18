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
        def closure(self):
            def func(target_self, key):
                item = object.__getattribute__(target_self, key)
                _nb_attrs = object.__getattribute__(target_self, '_nb_attrs')
                if key in _nb_attrs:
                    self.registry.add(target_self)
                return item
            return func

        cls.__getattribute__ = closure(self)

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
            yield from item._serialize(recurse=False)
