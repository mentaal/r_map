"""Functions for translating a register map to/from primitive objects which can
then be easily serialized into formats such as JSON"""
from r_map import Node

def decode_

def load(obj, parent=None, already_loaded=None, todo=None):
    if already_loaded is None:
        already_loaded = {}
    if todo is None:
        todo = {}
    if isinstance(obj, dict):
        #decode dict logic here
        pass
    elif 

def dump(node, already_dumped:dict=None):
    """Return a dictionary representing this object
    dump is called recursively to transform each Node object into a
    dictionary
    """
    if already_dumped is None:
        already_dumped = {}
    if node.uuid in already_dumped:
        return {'_ref' : o.uuid}
    dct = {n:getattr(node,n) for n in node._nb_attrs}
    dct['__type__'] = type(node).__name__
    ref = dct['_ref']
    if ref is not None:
        alias = dct['_alias']
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
        if len(node):
            dct['__children__'] = [c.dump(already_dumped) for c in node]
    already_dumped[node.uuid] = node

    #no need to add nulls
    return {k:v for k,v in dct.items() if v}





