from r_map.Register import Register
from r_map.SVGRegister import SVGRegister

def test_SVGRegister(data):
    reg = data.spi.cfg0

    svg = SVGRegister()

    svn_str = svg.to_svg(reg)
    with open('test_svg.svg', 'w') as F:
        F.write(svn_str)



