from random import randint, choice, choices
from string import ascii_letters, digits
from functools import partial
from r_map import BitField, Register, RegisterMap, Enumeration, BitFieldRef, Node

get_access = partial(choices, ('RW', 'RW1C', 'W', 'R', 'XX'), (100, 10, 20, 20, 20))

first_letter = ascii_letters
letters      = ascii_letters + digits


def get_names(amount, max_length=40):
    for iteration in range(amount):
        yield choice(first_letter) + ''.join(choice(letters)
                for i in range(1, randint(2, max_length)))

def get_data():
    #perform registration
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
                bf_ref = BitFieldRef(name=bf_name, parent=reg,
                        slice_width=bf_width, reg_offset=current_position)
                bf = BitField(name=bf_name, parent=bf_ref, width=bf_width,
                            access=get_access()[0])
                for value, enum_name in enumerate(get_names(amount=randint(1,4))):
                            Enumeration(parent=bf, name=enum_name, value=value)
                current_position += bf_width
                avail_width -= bf_width



    spi = RegisterMap(name='spi', parent=root, descr='A registermap defining the SPI block',
            local_address=0x40000000)
    cfgs = [Register(name=f'cfg{i}', parent=spi) for i in range(randint(10, 32))]

    def get_field(parent):
        remaining_width = 32
        current_position = 0
        field_index = 0
        while remaining_width:
            new_width = randint(1, remaining_width)
            bf_name = f'bf{field_index}'
            bf_ref = BitFieldRef(parent=parent,name=bf_name, slice_width=new_width,
                        reg_offset=current_position)
            yield  BitField(name=bf_name,
                    parent=bf_ref, width = new_width,
                    reset_val=randint(0, (1<<new_width)-1))
            if randint(0,100) > 60:
                break

            remaining_width -= new_width
            current_position += new_width
            field_index += 1


    for cfg in cfgs:
        available_width = 32
        bfs = [f for f in get_field(cfg)]
        if bfs:
            enum = Enumeration(name='spi_enabled', value=1, parent=bfs[0])
            enum2 = Enumeration(name='spi_disabled', value=0, parent=bfs[0])
    dodgy = RegisterMap(name='name', parent=root, descr='A dodgily named registermap!',
            local_address=0x50000000)

    return root
