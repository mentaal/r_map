from .Node import Node
class AddressedNode(Node):
    _nb_attrs = ('local_address',)
    def __init__(self, *args, local_address=0, **kwargs):
        '''Args:
            local_address(int): local address is the address of the node without
            consideration of any offset that a parent node may impose'''
        super().__init__(*args, **kwargs)
        self.local_address = local_address

    def __str__(self):
        return super().__str__() + ' ({:#010x})'.format(self.address)

    @property
    def address(self):
        if self.parent and hasattr(self.parent, 'address'):
            return self.local_address + self.parent.address #allows for relative addressing
        else:
            return self.local_address
    @address.setter
    def address(self, val):
        self.local_address = address

    def __dir__(self):
        d = super().__dir__()
        d.append('address')
        return d

