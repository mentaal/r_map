from .Register import Register
from lxml import etree as ET
from math import floor


class SVGRegister(Register):
    @staticmethod
    def stringify(d):
        return {k:str(v) for k,v in d.items()}
    def to_svg(self, reg):
        svg = ET.Element('svg', nsmap={
                None:"http://www.w3.org/2000/svg",
                'xlink':"http://www.w3.org/1999/xlink"})
        width       = 40
        height_incr = 50
        field_def_style = {'width':width, 'fill':'transparent', 'stroke':'black',
                'stroke-width':2}

        reg_base_x = 80
        reg_base_y = 10
        num_base_x = 40
        reset_num_base_x = reg_base_x + width//2

        reg_height = height_incr*reg.width
        fields_by_pos = {f.position:f for f in reg}
        border_attribs = field_def_style.copy()
        border_attribs.update(x=reg_base_x, y=reg_base_y, width=width,
                              height=reg_height)
        svg.append(ET.Element('rect', attrib=self.stringify(border_attribs)))

        #svg.append(ET.Comment(str(field)))

        txt_attribs = {'text-anchor':'middle'}


        for pos in range(reg.width):
            field = fields_by_pos.get(pos, None)
            if pos:
                y1 = y2 = reg_base_y+pos*height_incr
                line_attribs = {'x1':reg_base_x, 'y1':y1, 'x2':reg_base_x+width, 'y2':y2}
                if field is not None: #start of a new field
                    line_attribs['stroke'] = 'black'
                else:
                    line_attribs['stroke'] = 'blue'
                    line_attribs['stroke-dasharray'] = '2,2,2'
                svg.append(ET.Element('line', attrib=self.stringify(line_attribs)))
            pos_y_centre = int(pos*height_incr+height_incr/2)
            text_attribs = {'text-anchor':'middle',
                            'x': num_base_x,
                            'y': int(reg_base_y+pos*height_incr+height_incr*0.7),
                            'font-size': int(width*0.6)
                            }
            text_element = ET.Element('text', attrib=self.stringify(text_attribs))
            text_element.text = str(pos)
            svg.append(text_element)


            field_reset = field.reset if field else 'x'
            text_attribs['x'] = reset_num_base_x
            reset_element = ET.Element('text', attrib=self.stringify(text_attribs))
            reset_element.text = str(field_reset)
            svg.append(reset_element)

        svg_height = reg_height+reg_base_y+10
        svg_width  = reg_base_x + width + 10
        svg.set('viewBox', '0 0 {} {}'.format(svg_width, svg_height))
        #svg.set('preserveAspectRatio', 'xMinYMin meet')
        return ET.tostring(svg, pretty_print=True, encoding='unicode')

