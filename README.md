r_map
=====

A library for working with register map data.
The data source is abstracted such that if a user wants to work with a
particular data source, he/she may:

1. Provide an appropriately formatted serialized data source (probably the
   easiest)
2. Create a parser of the source data and dynamically generate the data
   structure using the provided data classes

Purpose
-------

1. Easily utilize register map data
2. Be able to iterate through register map from arbitrary position
3. Provide conveniences for walking through data
4. Provide ability to serialize/deserialize data
5. Provide mechanism to easily subclass base element implementations
6. Provide means to register which elements are accessed in data base and create
   a subtree from this data

Features
--------

Key and attribute access
------------------------

Key and attribute access to an elements sub elements. The key access is
particularly useful for cases where a sub element happens to have the name of a
reserved keyword in Python.

Example ::

    r_map1.reg.value = 10
    r_map1['reg'].value = 10

That elements are not intended to be added to a node via key based assignment
like a dictionary. A method: `_add` is provided for that.

Key based assignment is not intended to be supported because it can result in a
sub element having an alias which would be confusing and is an unlikely usecase.

Register to bitfield value mapping
----------------------------------

A register's value is based on its component bitfield's values. In fact, there
is an additional layer of indirection to support a register only having a
partial view to a bitfield. It's therefore possible for multiple registers to
have access to the same bitfield. Support for this level is complexity is baked
into the data structre and modelled with a class: BitFieldRef.

A full register map tree will look like this:

    Root (Node)
        rmap1 (RegisterMap)
            reg1 (Register)
                bitfield1_ref (BitFieldRef)
                    bitfield1 (BitField)
                        enum1 (Enumeration)
                        enum2 (Enumeration)
                        ...
                    bitfield2 (BitField)
                    ...
                bitfield2_ref (BitFieldRef)
                ....
            reg2 (Register)
            ....
        rmap2 (RegisterMap)
        ....

As in the above tree, it is possible that bitfield2_ref contains a reference to
bitfield1. Therefore reg1 and reg2 could both access the same bitfield.

Each bitfield also contains a `references` set which can be used to access all
of the BitFieldRef instances which point to it.

An example of where this would be quite useful is if the user extended the
BitField class to include a write method to write the BitField's value to a
piece of hardware. The bitfield is only accessible via the Registers which
reference it so the write function could then access the registers through the
BitFieldRef instances' parent attribute.

JSON
----

Support is provided to serialize the data structure to and from JSON using a
custom decoder and encoder.

Let's create some data:

```python

def get_basic_data():

    root = Node(name='root')

    r_map1 = RegisterMap(name='r_map1', parent=root, local_address=0x10000000,
            descr="An example register map containing registers")
    reg1 = Register(name='reg1', parent=r_map1, local_address=0x0)
    bf1_ref = BitFieldRef(name='bf1_ref', parent=reg1, slice_width=6,
                          field_offset=7, reg_offset=8)
    bf1 = BitField(name='bf1', parent=bf1_ref, width=20, reset=0x12345,
            access='RW', doc="Some documentation to describe the bitfield")
    enum1 = Enumeration(name='use_auto_inc', value=20, parent=bf1)
    enum2 = Enumeration(name='use_auto_dec', value=10, parent=bf1)

    reg2 = Register(name='reg2', parent=r_map1, local_address=0x4)
    bf2_ref = BitFieldRef(name='bf2_ref', parent=reg2, slice_width=4,
                          field_offset=3, reg_offset=4)
    bf2_ref.bf = bf1

    bf3_ref = BitFieldRef(name='bf3_ref', parent=reg2, slice_width=5,
                          field_offset=2, reg_offset=5)
    bf2 = BitField(name='bf2', parent=bf3_ref, width=20, reset=0x6789, access='R')
    bf4_ref = BitFieldRef(name='bf4_ref', parent=reg2, slice_width=2,
                          field_offset=0, reg_offset=0)
    bf4_ref._add(bf2)

    return root

```

And look at the following pytest testcase:

```python

def test_encode_to_json(basic_data):

    for obj in basic_data._walk(top_down=True, levels=-1):
        print(obj)

    json_data = to_json(basic_data, indent=4)
    print(json_data)

```

The printed tree looks like this:

    RegisterMap: r_map1 (0x10000000)
    Register: reg1 (0x10000000) value: 0x00000600
    BitFieldRef: bf1_ref
    BitField: bf1 width: 20, reset: 0x12345, value: 0x12345
    Enumeration: use_auto_inc value: 20
    Enumeration: use_auto_dec value: 10
    Register: reg2 (0x10000004) value: 0x000000c1
    BitFieldRef: bf2_ref
    BitField: bf1 width: 20, reset: 0x12345, value: 0x12345
    Enumeration: use_auto_inc value: 20
    Enumeration: use_auto_dec value: 10
    BitFieldRef: bf3_ref
    BitField: bf2 width: 20, reset: 0x06789, value: 0x06789
    BitFieldRef: bf4_ref
    BitField: bf2 width: 20, reset: 0x06789, value: 0x06789

The printed JSON looks like this:

```json

{
    "name": "root",
    "descr": null,
    "doc": null,
    "uuid": "2c0978ce1e614ea49c5ce9254f74d37a",
    "__type__": "Node",
    "children": [
        {
            "local_address": 268435456,
            "name": "r_map1",
            "descr": "An example register map containing registers",
            "doc": null,
            "uuid": "4f85ef8788dc4aec85eed44356329831",
            "__type__": "RegisterMap",
            "children": [
                {
                    "width": 32,
                    "local_address": 0,
                    "name": "reg1",
                    "descr": null,
                    "doc": null,
                    "uuid": "f17d456abeaa413983dbbf00e293e8f9",
                    "__type__": "Register",
                    "children": [
                        {
                            "slice_width": 6,
                            "reg_offset": 8,
                            "field_offset": 7,
                            "name": "bf1_ref",
                            "descr": null,
                            "doc": null,
                            "uuid": "7ea672aae3864045ae61a23497a41751",
                            "__type__": "BitFieldRef",
                            "children": [
                                {
                                    "width": 20,
                                    "reset": 74565,
                                    "access": "RW",
                                    "name": "bf1",
                                    "descr": null,
                                    "doc": "Some documentation to describe the bitfield",
                                    "uuid": "dadab6e82d5e4b6fafc69802791f4c9e",
                                    "__type__": "BitField",
                                    "children": [
                                        {
                                            "value": 20,
                                            "name": "use_auto_inc",
                                            "descr": null,
                                            "doc": null,
                                            "uuid": "d17aa40adbf3449c9fd965a7fe8cbc80",
                                            "__type__": "Enumeration"
                                        },
                                        {
                                            "value": 10,
                                            "name": "use_auto_dec",
                                            "descr": null,
                                            "doc": null,
                                            "uuid": "7c9d22efe9e246fdae55caa0a73cbaa1",
                                            "__type__": "Enumeration"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "width": 32,
                    "local_address": 4,
                    "name": "reg2",
                    "descr": null,
                    "doc": null,
                    "uuid": "61c89c4a8e714223a18678309e749e41",
                    "__type__": "Register",
                    "children": [
                        {
                            "slice_width": 4,
                            "reg_offset": 4,
                            "field_offset": 3,
                            "name": "bf2_ref",
                            "descr": null,
                            "doc": null,
                            "uuid": "f298ec5da3d04e62b8bda3d874625617",
                            "__type__": "BitFieldRef",
                            "children": [
                                {
                                    "__ref__": "dadab6e82d5e4b6fafc69802791f4c9e"
                                }
                            ]
                        },
                        {
                            "slice_width": 5,
                            "reg_offset": 5,
                            "field_offset": 2,
                            "name": "bf3_ref",
                            "descr": null,
                            "doc": null,
                            "uuid": "30cb3876b14743ea84770c39bafb3e64",
                            "__type__": "BitFieldRef",
                            "children": [
                                {
                                    "width": 20,
                                    "reset": 26505,
                                    "access": "R",
                                    "name": "bf2",
                                    "descr": null,
                                    "doc": null,
                                    "uuid": "c748c5715ab6410d9436c1e7fbfa7f33",
                                    "__type__": "BitField"
                                }
                            ]
                        },
                        {
                            "slice_width": 2,
                            "reg_offset": 0,
                            "field_offset": 0,
                            "name": "bf4_ref",
                            "descr": null,
                            "doc": null,
                            "uuid": "d699060c8e7549f8a1baec7778f15072",
                            "__type__": "BitFieldRef",
                            "children": [
                                {
                                    "__ref__": "c748c5715ab6410d9436c1e7fbfa7f33"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
```

The `__ref__` item in the JSON output indicates that it's a reference copy of
another object with the supplied UUID.





Notes
-----

1. the _nb_attrs class attribute is used to control what is serialized in each
   class instance.


