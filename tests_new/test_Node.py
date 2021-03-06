import r_map
def test_node_inst():
    node = r_map.Node(name='test_node')
    assert node.name == 'test_node'

def test_node_insertion():
    parent = r_map.Node(name='parent')
    child = r_map.Node(name='child')
    parent._add(child)
    assert child.parent == parent
    assert child in parent
    assert child.name in parent

def test_node_copy_uuid():
    n1 = r_map.Node(name='node')
    n2 = r_map.Node(name='node2')
    assert n1.uuid != n2.uuid
    n1_copy = n1._copy(uuid=n1.uuid)
    assert n1_copy.uuid == n1.uuid




