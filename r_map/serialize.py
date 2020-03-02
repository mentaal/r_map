"""Functions for serializing a register map to/from a flat dictionary"""
import r_map
from r_map import Node

"""schema:
{
    root: { #need a starting point
        type: xxx,
        children: [ <uuid>, ]
    },
    <uuid>: {
        name: xxx,
        type: xxx,
        <other metadata>,
        _ref: <uuid>,
        children: [ <uuid>, ]
    }
}
"""

def dump(node):
    dct = {}
    _dump(node, dct)
    dct['root'] = node.uuid
    return dct

def _dump(node, objs:dict):
    """Return a dictionary representing this object.
    """
    if node.uuid in objs:
        return
    my_uuid = node.uuid
    objs[my_uuid] = None #placeholder to prevent recursive calls serializing me
    dct = {n:getattr(node,n) for n in node._nb_attrs}
    dct.pop('uuid')
    dct['type'] = type(node).__name__
    ref = dct['_ref']
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
        objs[node.uuid] = dct
        _dump(ref, objs)
    elif isinstance(node, r_map.ArrayedNode):
        base_node = dct.pop('base_node')
        if base_node:
            dct['base_node'] = _dump(base_node, objs)
    elif len(node):
        dct['children'] = [_dump(c, objs) for c in node]

    #no need to add nulls
    objs[my_uuid] = {k:v for k,v in dct.items() if v is not None}
    return my_uuid

def load(dct:dict) -> Node:
    root_uuid = dct.get('root')
    if not root_uuid:
        raise ValueError("provided dictionary needs to contain a 'root'")
    return _load(root_uuid, dct, {})

def _load(my_uuid:str, dct:dict, already_loaded:dict) -> Node:
    if not isinstance(dct, dict):
        raise ValueError(f"Expected dictionary type argument. Got {type(dct)}")
    if my_uuid in already_loaded:
        return already_loaded[my_uuid]

    #decode dict logic here
    entry = dct[my_uuid]
    type_name = entry.get('type')
    T = getattr(r_map, type_name) if type_name else None
    ref_uuid = entry.get('_ref')
    if ref_uuid:
        ref_obj = already_loaded.get(ref_uuid, _load(ref_uuid, dct, already_loaded))
        vals = {k:v for k,v in entry.items() if k in ref_obj._nb_attrs
                                             and v is not None}
        obj = ref_obj._copy(alias=vals.pop('_alias', False),
                            **vals)
    elif T:
        vals = {k:v for k,v in entry.items() if k in T._nb_attrs
                                             and v is not None}

        if issubclass(T, r_map.ArrayedNode):
            vals['base_node'] = _load(vals['base_node'], dct, already_loaded)
        obj = T(**vals)
        children = entry.get('children')
        if children:
            for child_entry in children:
                child_obj = _load(child_entry,
                                 dct,
                                 already_loaded)
                obj._add(child_obj)
    else:
        raise ValueError(f"Could not _load data: {entry}")
    already_loaded[my_uuid] = obj
    return obj
