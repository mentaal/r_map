'''Hold some access descriptors used to simplify traversing the register map
data structure'''

class SubAccess():
    def __get__(self, instance, owner):

