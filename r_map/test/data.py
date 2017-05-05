from r_map.Node import Node
from r_map.Register import Register
from r_map.BitField import BitField
from r_map.RegisterMap import RegisterMap
from random import randint, choice
from string import ascii_letters, digits

first_letter = ascii_letters
letters      = ascii_letters + digits


def get_names(amount, max_length=40):
    for iteration in range(amount):
        yield choice(first_letter) + ''.join(choice(letters)
                for i in range(1, randint(2, max_length)))

def get_data():
    root = Node('root', None)
    for map_incr, rmap_name in enumerate(get_names(amount = randint(50, 100))):
        block = RegisterMap(rmap_name, root,
                local_address =0x40000000 + 0x1000*map_incr)
        for reg_incr, reg_name in enumerate(get_names(
                                                amount = randint(30, 200))):
            reg = Register(reg_name, block, local_address = 0x4*reg_incr)
            avail_width = 32
            current_position = 0
            for bf_incr, bf_name in enumerate(get_names(
                                                amount = randint(1, 33))):
                if avail_width <= 0:
                    break
                bf_width = randint(1, 33)
                if avail_width < bf_width:
                    bf_width = avail_width
                bf = BitField(bf_name, reg, width=bf_width,
                            position=current_position)
                current_position += bf_width
                avail_width -= bf_width



    spi = RegisterMap('spi', root, descr='A registermap defining the SPI block',
            local_address=0x40000000)
    cfgs = [Register('cfg{}'.format(i), spi) for i in range(10)]
    for cfg in cfgs:
        bfs = [BitField('bf{}'.format(i), cfg) for i in range(10)]
    dodgy = RegisterMap('name', root, descr='A dodgily name registermap!',
            local_address=0x50000000)

    return root
