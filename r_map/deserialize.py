from .Node import Node
def deserialize(d):
    objs = {}
    for uuid, node in d.items():
        node_copy = node.copy()
        _class = Node.class_registry[node_copy.pop('class_type')]
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



