"""Functions for translating a register map to/from primitive objects which can
then be easily serialized into formats such as JSON"""
from collections import deque
import r_map


def load(dct, parent=None, already_loaded=None, todo=None):
    if already_loaded is None:
        already_loaded = {}
    if todo is None:
        todo = deque()

    obj = _load(dct, parent=parent, already_loaded=already_loaded, todo=todo)
    #now finish loading by taking another pass
    while True:
        before_length = len(todo)
        if before_length == 0:
            break
        dct, parent = todo.popleft()
        _load(dct, parent=parent, already_loaded=already_loaded, todo=todo)
        after_length = len(todo)
        if after_length != before_length - 1:
            raise RuntimeError(f"Could not deserialize dictionary: {dct}"
                               f" with parent: {parent}")
    return obj


def _load(dct, parent, already_loaded, todo):
    obj = None
    if isinstance(dct, dict):
        #decode dict logic here
        type_name = dct.get('type')
        T = getattr(r_map, type_name) if type_name else None
        ref_uuid = dct.get('_ref')
        uuid = dct.get('uuid')
        if ref_uuid:
            ref_obj = already_loaded.get(ref_uuid)
            if ref_obj:
                vals = {k:v for k,v in dct.items() if k in ref_obj._nb_attrs
                                                   and v is not None}
                obj = ref_obj._copy(parent=parent,
                                    alias=vals.pop('_alias', False),
                                    **vals)
            else:
                todo.append((dct, parent))
                return
        elif uuid in already_loaded:
            obj = already_loaded[uuid]
        elif T:
            vals = {k:v for k,v in dct.items() if k in T._nb_attrs
                                               and v is not None}
            obj = T(parent=parent, **vals)
            children = dct.get('children')
            if children:
                for child_dct in children:
                    _load(child_dct,
                          parent=obj,
                          already_loaded=already_loaded,
                          todo=todo)
        else:
            raise ValueError(f"Could not load data: {dct}")
        already_loaded[obj.uuid] = obj
    else:
        raise ValueError(f"Expected dictionary type argument. Got {type(dct)}")
    return obj

def dump(node, already_dumped:dict=None):
    """Return a dictionary representing this object
    dump is called recursively to transform each Node object into a
    dictionary
    """
    if already_dumped is None:
        already_dumped = {}
    if node.uuid in already_dumped:
        dct = {'_ref' : node.uuid}
        if node._alias:
            dct['_alias'] = node._alias
        return dct
    dct = {n:getattr(node,n) for n in node._nb_attrs}
    dct['type'] = type(node).__name__
    ref = dct['_ref']
    base_node = dct.get('base_node')
    if base_node:
        dct['base_node'] = dump(base_node, already_dumped)
    if ref is not None:
        dct['_ref'] = ref.uuid
        #only save overridden values
        keys = node._nb_attrs - set(['_ref', '_alias'])
        for k in keys:
            if k in dct and hasattr(ref, k):
                dct_val = dct[k]
                ref_val = getattr(ref, k)
                if dct_val == ref_val:
                    dct.pop(k)

    else:
        if len(node) and not isinstance(node, r_map.ArrayedNode):
            dct['children'] = [dump(c, already_dumped) for c in node]
    already_dumped[node.uuid] = node

    #no need to add nulls
    return {k:v for k,v in dct.items() if v is not None}





