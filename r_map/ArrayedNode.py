import re
from functools import partial, reduce
from operator import ior
import r_map
from .Node import Node

class ArrayedNode(Node):
    '''A node that is used to hold an arrayed definition of instances.

    The instances could be of various types such as RegisterMap, Register and
    BitField. If `_ref` is not None, it should only be of type ArrayedNode.
    When this is the case, the `base_node` attribute isn't used and instead the
    base node is sourced from the `_ref` object.
    '''
    _nb_attrs = frozenset(['start_index', 'incr_index', 'end_index',
                           'increment', 'base_val', 'base_node', 'array_letter'])
    def __init__(self, *, start_index=0, incr_index=1, end_index=1,
                 increment=1, array_letter='n', **kwargs):

        super().__init__(start_index=start_index, incr_index=incr_index,
                         end_index=end_index, increment=increment, **kwargs)
        self.index_re = re.compile(rf'\[{array_letter}+\]')
        self.base_name = self.index_re.sub('', self.name)
        self._range_val = range(start_index, end_index, incr_index)
        self._make_repl_func = lambda i:lambda m:f'{i:0{m.end()-m.start()-2}}'
        #get a spec for getting the index from an argument name
        iter_spans = ((i*2, m.span()) for i,m in
                enumerate(self.index_re.finditer(self.name or '')))
        #subtractions here are to cater for removal of brackets
        self._parse_specs = [(x[0]-i, x[1]-i-2) for i,x in iter_spans]

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
                name, index = self._parse_name(item)
            except ValueError:
                return False
            return name == self.base_name
        else:
            return super().__contains__(item)

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
        sub = partial(self.index_re.sub, repl=self._make_repl_func(index))
        instance_name = sub(string=self.name or '')

        inst = self._children.get(instance_name)
        if not inst:
            key = 'local_address' if isinstance(self.base_node,
                                                r_map.AddressedNode) else \
                   'reg_offset'
            inc = (index//self.incr_index)*self.increment + self.base_val
            kwargs = {key:inc}

            #if we're an alias, treat the dynamically created inst from _ref as
            #the base node
            if self._alias:
                base_node = self._ref._load_instance(index)
            else:
                base_node = self.base_node

            inst = self.base_node._copy(
                    parent=self,
                    name=instance_name,
                    descr=sub(string=self.descr or ''),
                    doc=sub(string=self.doc or ''),
                    alias=self._alias,
                    **kwargs)
            self._children[instance_name] = inst
        return inst

    def __iter__(self):
        return (self._load_instance(i) for i in self._range_val)

    def _parse_name(self, item:str):
        name = ''.join(self._around_spans(item, self._parse_specs))
        index = int(item[slice(*self._parse_specs[0])])
        return name, index

    def __getitem__(self, item):
        if isinstance(item, str):
            if item in self._children:
                return self._children[item]
            elif item in self:
                name, index = self._parse_name(item)
                return self._load_instance(index)
            else:
                raise KeyError(item)
        elif isinstance(item,int):
            return self._load_instance(item)
        else:
            raise NotImplemented

    def _copy(self, *, deep_copy=True, alias=False, **kwargs):
        """Create a deep copy of this object
        Implementation within this class is almost the same as that from Node.
        The difference is that children of this object are dynamically generated
        and should never be copied.
        """
        #always pass deep_copy=False here because we never want to copy children
        #in an ArrayedNode
        new_obj = super()._copy(alias=alias, deep_copy=False, **kwargs)
        return new_obj

