from collections import OrderedDict as OD
from uuid import uuid4
from itertools import chain
from operator import attrgetter
import logging
logger = logging.getLogger(__name__)

class NodeMeta(type):
    '''used to magically update the nb_attrs'''
    def __new__(mcs, name, bases, attrs):
        _nb_attrs = attrs.get('_nb_attrs', frozenset())
        for b in bases:
            if hasattr(b, '_nb_attrs'):
                _nb_attrs |= b._nb_attrs
        attrs['_nb_attrs'] = _nb_attrs

        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class

class Node(metaclass=NodeMeta):
    '''A node in the tree data structure representing the register map'''
    #these names are not to be looked for in children
    #when pickling, only be concerned with these
    _nb_attrs = frozenset(['name', 'descr', 'doc', 'uuid', '_ref', '_alias'])

    def __init__(self, *, parent=None, **kwargs):
        '''
        Args:
            name(str)      : A the name of the Node
            parent(Node)   : Either a Node or None
            descr(str)     : A description for the node (usually shorter than doc)
            doc(str)       : A documentation string for the node
            uuid(str)      : A Universal Identifier
            _ref(Node)     : Either a Node or None
            _alias(bool)   : Indicating if the node is an instance (False) or
                             alias (True)
        '''
        for key in self._nb_attrs:
            setattr(self, key, kwargs.get(key, None))

        self._children = {}
        self._parent = None
        self.parent = parent
        self.__doc__ = next((i for i in (self.descr, self.doc) if i), 'No description')
        self.uuid = kwargs.get('uuid', uuid4().hex)

        unexpecteds = kwargs.keys() - self._nb_attrs
        if unexpecteds:
            raise ValueError("Got unexpected keyword arguments: {}".format('\n'.join(unexpecteds)))

    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self, val):
        if val is None:
            #uninstall self from parent as well
            p = self._parent
            if p:
                if self in p:
                    p._children.pop(self.name)
            self._parent = None
        elif val is not None and not isinstance(val, Node):
            raise ValueError("Parent node needs to be of type Node or NoneType")
        else:
            self._parent = val
            if self not in val:
                val._add(self)

    def __str__(self):
        return f'{type(self).__name__}: {self.name}'

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._children
        else:
            return item in self._children.values()

    def __dir__(self):
        local_items = {f for f in vars(self) if f[0] != '_'}
        children    = {c for c in self._children}
        class_objs  = {s for s in dir(type(self)) if s[0] != '_'}
        return list(local_items | children | class_objs)

    def __getattr__(self, name):
        if name in self._nb_attrs or name[:2] == '__':
            raise AttributeError(f"{name} not found")
        try:
            return self._children[name]
        except (KeyError, AttributeError) as e:
            raise AttributeError(f"{name} not found")

    def __getitem__(self, item):
        return self._children[item]

    def _add(self, item):
        if item in self:
            return #already added
        elif item.name in self:
            item.parent = None #maintain consistency as we're replacing an existing item
        self._children[item.name] = item

    def __iter__(self):
        return (child for child in self._children.values())

    def _walk(self, levels=2, top_down=True, expand_arrayed=True):
        'return up to <levels> worth of nodes'
        if levels == 0: #i am a leaf node
            yield self
            return
        if top_down:
            yield self
        for node in self:
            #if a negative number is supplied, all elements below will be traversed
            if levels >= 0:
                new_levels = levels -1
            else:
                new_levels = levels
            yield from node._walk(levels=new_levels, top_down=top_down)
        if not top_down:
            yield self

    def __bool__(self):
        return True #don't call __len__

    def __len__(self):
        return len(self._children)

    def __repr__(self):
        items = ((k,getattr(self, k)) for k in self._nb_attrs)
        me = {k:v for (k,v) in items if v is not None}

        arg_strings = (f'{k}={v}' for (k,v) in sorted(me.items(),
            key=lambda x:x[0]))
        return f"{type(self).__name__}({','.join(arg_strings)})"

    def _copy(self, *, parent=None, alias=False, deep_copy=True, **kwargs):
        """A create a deep copy of this object
        :param parent: The parent obj
        :param alias: Indicate if the copy should be an alias. This means that
                      any children of the new copy which happens to be bitfields
                      won't be copies but references of this node. This
                      attribute is passed down through the node hierarchy and is
                      used by BitFieldRef instances to determine if a copy of
                      its Bitfield child should be made.
        :deep_copy: Create a deep copy of this instance. 
        """
        existing_items = {k:getattr(self, k) for k in self._nb_attrs}
        #It's a copy so shouldn't have the same uuid
        existing_items.pop('uuid', None)
        existing_items.update(kwargs)
        existing_items['parent'] = parent
        existing_items['_ref'] = self
        existing_items['_alias'] = alias
        new_obj = type(self)(**existing_items)
        if deep_copy:
            for obj in self:
                obj._copy(parent=new_obj, alias=alias)
        return new_obj

    def validate(self):
        """Do some validation checks on the parameters set on this instance and
        that of the child bitfield

        :returns: Iterable of errors found
        """
        for child in self:
            yield from child.validate()




