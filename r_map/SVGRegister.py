from .Register import Register
from lxml import etree as ET

class SVGRegister(Register):
    def to_svg(self, reg):
        svg = ET.Element('svg', nsmap={
                None:"http://www.w3.org/2000/svg",
                'xlink':"http://www.w3.org/1999/xlink"})
        height_incr = 50
        field_def_style = {'width':'40', 'fill':'transparent', 'stroke':'black',
                'stroke-width':'2'}

        base_x = 10
        base_y=10
        for field in sorted(reg, key=lambda x:x.position):

            field_height = height_incr*field.width
            attribs = dict(x=str(base_x), y=str(base_y),
                    height=str(field_height))
            attribs.update(field_def_style)
            svg.append(ET.Element('rect', attrib=attribs))
            svg.append(ET.Comment(str(field)))

            base_y += field_height
        svg.attrib['width'] = '50'
        svg.attrib['height'] = str(base_y+30)
        return ET.tostring(svg, pretty_print=True, encoding='unicode')

