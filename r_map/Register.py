from .AddressedNode import AddressedNode
class Register(AddressedNode):
    _nb_attrs = ('width', 'reset')
    def __init__(self, *args, width=32, reset=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.width   = width
        self.reset   = reset
        self.value = reset



