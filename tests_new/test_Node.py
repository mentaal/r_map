import r_map
def test_node_inst():
    node = r_map.Node(name='test_node')
    assert node.name == 'test_node'

def test_node_insertion():
    parent = r_map.Node(name='parent')
    child = r_map.Node(name='child', parent=parent)
    assert child.parent == parent
    assert child in parent
    assert child.name in parent




