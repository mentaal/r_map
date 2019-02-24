"""
Module to provide functionality to serialize and deserialize r_map data to JSON.
A custom encoder/decoder is implemented to facilitate this.
"""
import json
import r_map
from collections import defaultdict, ChainMap

class RMapJSONParseError(KeyError):
    pass

class RMapJSON(json.JSONEncoder):
    already_encoded = {}
    def default(self, o):
        if isinstance(o, r_map.Node):
            if o.uuid in self.already_encoded:
                return {'_ref' : o.uuid}
            dct = {n:getattr(o,n) for n in o._nb_attrs}
            dct['__type__'] = type(o).__name__
            ref = dct['_ref']
            if ref is not None:
                alias = dct['_alias']
                dct['_ref'] = ref.uuid
                #only save overridden values
                keys = o._nb_attrs - set(['_ref', '_alias'])
                for k in keys:
                    if k in dct and hasattr(ref, k):
                        dct_val = dct[k]
                        ref_val = getattr(ref, k)
                        if dct_val == ref_val:
                            dct.pop(k)

            else:
                if len(o):
                    dct['__children__'] = list(o)
            self.already_encoded[o.uuid] = o

            #no need to add nulls
            return {k:v for k,v in dct.items() if v}
        elif isinstance(o, set):
            return list(o)
        else:
            return json.JSONEncoder.default(self, o)

def to_json(node, **kwargs):
    RMapJSON.already_encoded.clear()
    return json.dumps(node, cls=RMapJSON, **kwargs)

def from_json(json_str, **kwargs):
    decoder, decoded, todo = get_decoder()

    root = json.loads(json_str, object_hook=decoder, **kwargs)

    #now finish up the decoding process
    for parent_uuid, ref_list in todo.items():
        try:
            parent = decoded[parent_uuid]
        except KeyError as e:
            raise RMapJSONParseError("Cannot find object with uuid: {} "
                                     "which is referenced by another node".format(
                                         parent_uuid)) from e
        for ref_uuid in ref_list:
            try:
                ref_obj = decoded[ref_uuid]
            except KeyError as e:
                raise RMapJSONParseError("Cannot find object with uuid: {} "
                         "referenced from parent {} with uuid: {}".format(
                         ref_uuid, parent, parent_uuid))
            parent._add(ref_obj)
            ref_obj.parent = parent

    return root

def get_decoder():
    """Create a closure to hold a dictionary of already decoded items"""
    #This strategy might need to be revised to allow a root node to be deferred
    #to the todo list
    decoded = {}
    todo = defaultdict(list)
    def decoder(dct):
        if '__type__' in dct:
            ref_uuid = dct.get['_ref']
            if ref_uuid is not None:
                if ref_uuid not in decoded:
                    todo['_root'].append(dct)
                    return dct
                else:
                    ref_obj = decoded[ref_uuid]
                    obj_map = ChainMap(dct, ref_obj.__dict__)
            else:
                obj_map = dct
            #print("In decoder, dct: ", dct)
            #if dct.get('_alias'):
            obj_type = getattr(r_map, dct.pop('__type__'))
            obj = obj_type(**{k:obj_map.get(k) for k in obj_type._nb_attrs})
            decoded[obj.uuid] = obj
            if 'children' in dct:
                for child in dct['children']:
                    if isinstance(child, dict):
                        ref = child.get('_ref')
                        if ref:
                            parent_uuid = obj.uuid
                            todo[parent_uuid].append(ref)
                    else:
                        obj._add(child)
                        child.parent = obj
            return obj
        else:
            return dct
    return decoder, decoded, todo



