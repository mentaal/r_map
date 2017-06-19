from collections import OrderedDict as OD
from uuid import uuid4
from itertools import chain
from operator import attrgetter
import logging
logger = logging.getLogger(__name__)

class Registry():
    """Registry used to hold mappings of register map elements to class
    implementations"""
    registry = {}

    def __get__(self, instance, owner):
        return self.registry

    def __set__(self, instance, value):
        raise AttributeError("Cannot set attribute - read only")

class NodeMeta(type):
    '''used to magically update the nb_attrs'''
    def __new__(mcs, name, bases, attrs):
        _nb_attrs = attrs.get('_nb_attrs', ())
        for b in bases:
            if hasattr(b, '_nb_attrs'):
                _nb_attrs += b._nb_attrs
            if hasattr(b, '_class_registry'):
                if '_class_registry' not in attrs:
                    attrs['_class_registry'] = b.__dict__['_class_registry']
        attrs['_nb_attrs'] = _nb_attrs
        if '_class_registry' not in attrs:
            #make a read-only data descriptor to prevent user from clobbering
            #registry
            attrs['_class_registry'] = Registry()
        r = attrs['_class_registry'].registry

        new_class = super().__new__(mcs, name, bases, attrs)
        if name not in r and name == 'Node':
            #only automatically register the base class
            r[name] = new_class
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
            descr(str)  : A description for the node (usually shorter than doc)
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
        if descr:
            self.__doc__ = descr
        elif doc:
            self.__doc__ = doc

        if uuid is None:
            self.uuid = uuid4().hex
        else:
            self.uuid = uuid


    def __str__(self):
        return '{}: {}'.format(type(self).__name__,self.name)


    def __dir__(self):
        local_files = {f for f in vars(self) if f[0] != '_'}
        children    = {c for c in self._children}
        class_objs  = {s for s in dir(type(self)) if s[0] != '_'}
        return list(local_files | children | class_objs)

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

    def _walk(self, levels=2, top_down=True):
        'return up to <levels> worth of nodes'
        if levels == 0: #i am a leaf node
            yield self
            return
        if top_down:
            yield self
        for node in self:
            if levels >= 0:
                #if a negative number is supplied, all elements below will be traversed
                levels -= 1
            yield from node._walk(levels=levels, top_down=top_down)
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

    def _serialize(self, recurse=True):
        #sg = attrgetter(*self._nb_attrs)
        items = ((k,getattr(self, k)) for k in self._nb_attrs)
        me = {k:v for (k,v) in items if v is not None}
        me['class_type'] = type(self).__name__
        #change the parent from being an object reference to a uuid reference
        if self.parent:
            me['parent'] = self.parent.uuid
        if recurse:
            for node in self:
                yield from node._serialize()
        yield self.uuid, me

    @classmethod
    def _deserialize(cls, d):
        objs = {}
        for uuid, node in d.items():
            node_copy = node.copy()
            _class = cls._class_registry[node_copy.pop('class_type')]
            objs[uuid] = _class(uuid=uuid, **node_copy)

        root = None
        #now walk through all the items again and setup node references
        for uuid, node in objs.items():
            parent_uuid = node.parent
            if parent_uuid != None:
                try:
                    parent_node = objs[parent_uuid]
                except KeyError as e:
                    raise KeyError(
                        "Can't find parent for node: {} (parent={})".format(node,
                            parent_uuid))
                parent_node[node.name] = node
                node.parent = parent_node

            else: #this node is the root
                root = node
                root.parent = None
            #print('Now on node: {}, parent: {}'.format(node, node.parent))
        if root is None:
            raise KeyError("Could not find the root node!")
        return root

    @classmethod
    def _register(cls, name=None):
        '''Register derived class with base class. Name is optional and if
        omitted, defaults to the derived class' name'''
        if name is None:
            name = cls.__name__
        logger.debug("Registering: %s under name: %s", cls, name)
        cls._class_registry[name] = cls


    @classmethod
    def _register_default_classes(cls):
        print("Registering default classes...")
        import importlib
        class_names = ('Register', 'RegisterMap', 'BitField')
        for c_str in class_names:
            module = importlib.import_module('.'+c_str, 'r_map')
            c = getattr(module, c_str)
            c._register()



