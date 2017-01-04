from collections import OrderedDict as OD
from uuid import uuid4
from itertools import chain
from operator import attrgetter
class NodeMeta(type):
    '''used to magically update the nb_attrs'''
    def __new__(mcs, name, bases, attrs):
        _nb_attrs = attrs.get('_nb_attrs', ())
        if name == 'Node':
            attrs['class_registry'] = {}
        for b in bases:
            if hasattr(b, '_nb_attrs'):
                _nb_attrs += b._nb_attrs
        attrs['_nb_attrs'] = _nb_attrs
        new_class = super().__new__(mcs, name, bases, attrs)
        new_class.class_registry[name] = new_class
        return new_class

class Node(metaclass=NodeMeta):
    '''A node in the tree data structure representing the register map'''
    #these names are not to be looked for in children
    #when pickling, only be concerned with these
    _nb_attrs = ('name', 'descr', 'doc')


    def __init__(self, name, parent=None, descr=None, doc=None, uuid=None):
        '''
        Args:
            name(str)   : A the name of the Node
            parent(Node): Either a Node or None
            descr(str)  : A description for the node
            doc(str)    : A documentation string for the node
        '''
        self.name     = name
        self.parent   = parent
        self.descr    = descr
        self.doc      = doc
        #automatically install it in the parent
        if self.parent and isinstance(self.parent, Node):
            self.parent[name] = self
        self._children = OD()

        if uuid is None:
            self.uuid = uuid4().hex
        else:
            self.uuid = uuid


    def __str__(self):
        return '{}: {}'.format(type(self).__name__,self.name)


    def __dir__(self):
        local_files = [f for f in self.__dict__ if f[0] != '_']
        children    = [c for c in self._children]
        return local_files + children

    def __getattr__(self, name):
        if name in self._nb_attrs or name[:2] == '__':
            raise AttributeError(name)
        try:
            return self._children[name]
        except (KeyError, AttributeError) as e:
            raise AttributeError(name)

    def __getitem__(self, item):
        return self._children[item]

    def __setitem__(self, name, item):
        self._children[name] = item

    def __iter__(self):
        return (child for child in self._children.values())

    def _serialize(self):
        #sg = attrgetter(*self._nb_attrs)
        items = ((k,getattr(self, k)) for k in self._nb_attrs)
        me = {k:v for (k,v) in items if v is not None}
        #print('me dictionary: ', me)
        me['class_type'] = type(self).__name__
        #change the parent from being an object reference to a uuid reference
        if self.parent:
            me['parent'] = self.parent.uuid
        for node in self:
            yield from node._serialize()
        yield self.uuid, me

    def walk(self, levels=2, top_down=True):
        'return up to <levels> worth of nodes'
        if levels == 0: #i am a leaf node
            yield self
            return
        if top_down:
            yield self
        for node in self:
            yield from node.walk(levels=levels-1, top_down=top_down)
        if not top_down:
            yield self

    def __bool__(self):
        return True #don't call __len__

    def __len__(self):
        return len(self._children)

    def __repr__(self):
        items = ((k,getattr(self, k)) for k in self._nb_attrs)
        me = {k:v for (k,v) in items if v is not None}

        arg_strings = ('{}={}'.format(k,v) for (k,v) in sorted(me.items(),
            key=lambda x:x[0]))
        return '{}({})'.format(type(self).__name__, ','.join(arg_strings))

