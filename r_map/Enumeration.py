from .Node import Node
class Enumeration(Node):
    _nb_attrs = ('value',)

    def __str__(self):
        return super().__str__() + ' value: {}'.format(self.value)


