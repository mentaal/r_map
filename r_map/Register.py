from .AddressedNode import AddressedNode
class Register(AddressedNode):
    _nb_attrs = ('width', 'reset')
    def __init__(self, width=32, reset=0, **kwargs):
        super().__init__(width=width, reset=reset, **kwargs)
        self.value = reset

    @property
    def access(self):
        print("eh?")
        return '|'.join(sorted(set(o.access for o in self._children.values())))


