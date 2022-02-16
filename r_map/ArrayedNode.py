import re
from functools import partial, reduce
from operator import ior
import r_map
from .Node import Node
from .arrayed_node_name_parser import make_parser

class ArrayedNode(Node):
    '''A node that is used to hold an arrayed definition of instances.

    The instances could be of various types such as RegisterMap, Register and
    BitField. If `_ref` is not None, it should only be of type ArrayedNode.
    When this is the case, the `base_node` attribute isn't used and instead the
    base node is sourced from the `_ref` object.

    .. note::
        Currently, it is not supported to have an ArrayedNode contain an
        ArrayedNode
    '''
    _nb_attrs = frozenset(['start_index', 'incr_index', 'end_index',
                           'increment', 'base_val', 'base_node', 'array_letter'])
    def __init__(self, *, name, start_index=0, incr_index=1, end_index=1,
                 increment=1, array_letter='n', **kwargs):

        self._range_val = range(start_index, end_index, incr_index)
        self.name_gen, self._parse_name = make_parser(self._range_val, array_letter, name)
        index_re = re.compile(rf'\[{array_letter}+\]')
        self._make_repl_func = lambda i:lambda m:f'{i:0{m.end()-m.start()-2}}'
        self.index_re = index_re
        _ugly_name, _full_name = index_re.sub('', name), name
        name = _ugly_name.strip('_')
        super().__init__(name=name, start_index=start_index, incr_index=incr_index,
                         end_index=end_index, increment=increment,
                         array_letter=array_letter, **kwargs)
        self._full_name = _full_name

        if self._ref:
            self.base_node = self._ref.base_node

    @staticmethod
    def _around_spans(s, spans):
        """Given a string and spans, return the string around the spans"""
        i = 0
        for start,end in spans:
            if i < start:
                yield s[i:start]
                i = start
            if i < end:
                i = end
        yield s[i:len(s)]

    def __contains__(self, item):
        if isinstance(item, str):
            try:
                index = self._parse_name(item)
            except ValueError:
                return False
            return index is not None
        else:
            return super().__contains__(item)

    @property
    def address(self):
        if self.parent and hasattr(self.parent, 'address'):
            return self.base_val + self.parent.address #allows for relative addressing
        else:
            return self.base_val

    @property
    def value(self):
        if isinstance(self.base_node, r_map.BitFieldRef):
            return reduce(ior, (f.value for f in self), 0)
        else:
            raise TypeError("value is not a meaningful property on an "
                    "ArrayedNode with a base_node of type: "
                    f"{type(self.base_node)}")

    @value.setter
    def value(self, x):
        if isinstance(self.base_node, r_map.BitFieldRef):
            for f in self:
                f.value = x
        else:
            raise TypeError("value is not a meaningful property on an "
                    "ArrayedNode with a base_node of type: "
                    f"{type(self.base_node)}")

    def _load_instance(self, index):
        """Helper for lazy loading requested instance. When instance is not
        present in children, this method gets called to create it
        """
        if index not in self._range_val:
            raise IndexError(f"Requested item with index: {index} out of range:"
                             f" {self._range_val}")
        instance_name = self.name_gen(index)

        inst = self._children.get(instance_name)
        bn = self.base_node
        bn_is_arrayed = isinstance(bn, r_map.ArrayedNode)
        if not inst:
            num_inc = (index - self.start_index) // self.incr_index
            if isinstance(bn, r_map.AddressedNode):
                key = 'local_address'
                inc = num_inc*self.increment
            elif isinstance(bn, r_map.BitFieldRef):
                key = 'reg_offset'
                inc = num_inc*self.increment + self.base_val
            elif bn_is_arrayed:
                key = 'base_val'
                inc = num_inc*self.increment
            else:
                raise ValueError(f"Unsupported base node type: {type(bn)} for Arrayed Register: {self}")

            kwargs = {key:inc}

            #if we're an alias, treat the dynamically created inst from _ref as
            #the base node
            if self._alias:
                base_node = self._ref._load_instance(index)
            else:
                base_node = self.base_node

            if bn_is_arrayed:
                name_for_copy = bn._full_name
            else:
                name_for_copy = instance_name

            sub = partial(self.index_re.sub, repl=self._make_repl_func(index))

            inst = base_node._copy(
                    name=name_for_copy,
                    descr=sub(string=self.descr or ''),
                    doc=sub(string=self.doc or ''),
                    new_alias=self._alias,
                    **kwargs)

            if bn_is_arrayed:
                # update the instance name after it has been created if it's an
                # arrayed node so we don't mess up it's name handling but still
                # allow it to have a meaningful name
                inst.name = instance_name
            self._add(inst)
        return inst

    def __iter__(self):
        return (self._load_instance(i) for i in self._range_val)

    def __getitem__(self, item):
        if isinstance(item, str):
            if item in self._children:
                return self._children[item]
            else:
                try:
                    index = self._parse_name(item)
                except ValueError:
                    raise KeyError(item)
                return self._load_instance(index)
        elif isinstance(item,int):
            return self._load_instance(item)
        else:
            raise NotImplemented

    def _copy(self, *, _deep_copy=True, new_alias=False, **kwargs):
        """Create a deep copy of this object
        Implementation within this class is almost the same as that from Node.
        The difference is that children of this object are dynamically generated
        and should never be copied.
        """
        #always pass deep_copy=False here because we never want to copy children
        #in an ArrayedNode
        name_update = kwargs.pop('name', self._full_name)
        new_obj = super()._copy(new_alias=new_alias, _deep_copy=False,
                name=name_update, **kwargs)
        if new_obj.base_node == None:
            new_obj.base_node = self.base_node
        return new_obj

    def __getattr__(self, name):
        if name in ('reg_offset', 'local_address'):
            return self.base_val
        else:
            try:
                return super().__getattr__(name)
            except AttributeError as e:
                try:
                    index = self._parse_name(name)
                except ValueError:
                    raise e
                if index is not None:
                    return self._load_instance(index)
                else:
                    raise e

    def __len__(self):
        return len(range(self.start_index, self.end_index, self.incr_index))

