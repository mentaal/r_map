from r_map.Node import Node
from r_map.Register import Register
from r_map.BitField import BitField
from r_map.RegisterMap import RegisterMap
from r_map.Enumeration import Enumeration
from random import randint, choice, choices
from string import ascii_letters, digits
from functools import partial

get_access = partial(choices, ('RW', 'RW1C', 'W', 'R', 'XX'), (100, 10, 20, 20, 20))

first_letter = ascii_letters
letters      = ascii_letters + digits


def get_names(amount, max_length=40):
    for iteration in range(amount):
        yield choice(first_letter) + ''.join(choice(letters)
                for i in range(1, randint(2, max_length)))

def get_data():
    #perform registration
    Node._register_default_classes()
    root = Node(name='root')
    for map_incr, rmap_name in enumerate(get_names(amount = randint(20, 50))):
        block = RegisterMap(name=rmap_name, parent=root,
                local_address =0x40000000 + 0x1000*map_incr)
        for reg_incr, reg_name in enumerate(get_names(
                                                amount = randint(10, 100))):
            reg = Register(name=reg_name, parent=block, local_address = 0x4*reg_incr)
            avail_width = 32
            current_position = 0
            for bf_incr, bf_name in enumerate(get_names(
                                                amount = randint(1, 33))):
                if avail_width <= 0:
                    break
                bf_width = randint(1, 33)
                if avail_width < bf_width:
                    bf_width = avail_width
                bf = BitField(name=bf_name, parent=reg, width=bf_width,
                            position=current_position, access=get_access()[0])
                for value, enum_name in enumerate(get_names(amount=randint(1,4))):
                            Enumeration(parent=bf, name=enum_name, value=value)
                current_position += bf_width
                avail_width -= bf_width



    spi = RegisterMap(name='spi', parent=root, descr='A registermap defining the SPI block',
            local_address=0x40000000)
    cfgs = [Register(name='cfg{}'.format(i), parent=spi) for i in range(10)]
    for cfg in cfgs:
        bfs = [BitField(name='bf{}'.format(i), parent=cfg) for i in range(10)]
        enum = Enumeration(name='spi_enabled', value=1, parent=bfs[0])
        enum2 = Enumeration(name='spi_disabled', value=0, parent=bfs[0])
    dodgy = RegisterMap(name='name', parent=root, descr='A dodgily name registermap!',
            local_address=0x50000000)

    return root
