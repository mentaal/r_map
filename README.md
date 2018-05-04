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

Let's look at the following pytest testcase:

```python

def test_encode_to_json(basic_data):

    #first get a copy
    new_data = basic_data._copy()
    r_map1 = new_data.r_map1

    #make a reference copy
    r_map1['reg3'] = r_map1.reg2

    for obj in new_data._walk(top_down=True, levels=-1):
        print(obj)

    json_data = to_json(new_data, indent=4)
    print(json_data)

```

The printed tree looks like this:

>Node: root
>RegisterMap: r_map1 (0x10000000)
>Register: reg1 (0x10000000) value: 0x00000600
>BitFieldRef: bf1_ref
>BitField: bf1 width: 20, reset: 0x12345, value: 0x12345
>Enumeration: use_auto_inc value: 20
>Enumeration: use_auto_dec value: 10
>Register: reg2 (0x10000004) value: 0x00000080
>BitFieldRef: bf2_ref
>BitField: bf1 width: 20, reset: 0x12345, value: 0x12345
>Enumeration: use_auto_inc value: 20
>Enumeration: use_auto_dec value: 10
>Register: reg2 (0x10000004) value: 0x00000080
>BitFieldRef: bf2_ref
>BitField: bf1 width: 20, reset: 0x12345, value: 0x12345
>Enumeration: use_auto_inc value: 20
>Enumeration: use_auto_dec value: 10

The printed JSON looks like this:

>{
>    "name": "root",
>    "descr": null,
>    "doc": null,
>    "uuid": "c94ccefb139246cc9b7551dce5475d53",
>    "__type__": "Node",
>    "children": [
>        {
>            "local_address": 268435456,
>            "name": "r_map1",
>            "descr": "An example register map containing registers",
>            "doc": null,
>            "uuid": "c2542b43075442a7b32086376f7601b8",
>            "__type__": "RegisterMap",
>            "children": [
>                {
>                    "width": 32,
>                    "local_address": 0,
>                    "name": "reg1",
>                    "descr": null,
>                    "doc": null,
>                    "uuid": "3173a181fcd3406db8531c2d814a0e42",
>                    "__type__": "Register",
>                    "children": [
>                        {
>                            "slice_width": 6,
>                            "reg_offset": 8,
>                            "field_offset": 7,
>                            "name": "bf1_ref",
>                            "descr": null,
>                            "doc": null,
>                            "uuid": "cc9aee9525c740908d5686e36acdab2f",
>                            "__type__": "BitFieldRef",
>                            "children": [
>                                {
>                                    "width": 20,
>                                    "reset": 74565,
>                                    "access": "RW",
>                                    "name": "bf1",
>                                    "descr": null,
>                                    "doc": null,
>                                    "uuid": "884cc624b8c949af9c95f1b0a749c4de",
>                                    "__type__": "BitField",
>                                    "children": [
>                                        {
>                                            "value": 20,
>                                            "name": "use_auto_inc",
>                                            "descr": null,
>                                            "doc": null,
>                                            "uuid": "d4042bec7cff443781d9281931bfa791",
>                                            "__type__": "Enumeration"
>                                        },
>                                        {
>                                            "value": 10,
>                                            "name": "use_auto_dec",
>                                            "descr": null,
>                                            "doc": null,
>                                            "uuid": "25b9f2e954d244b8a8ea09523f271afd",
>                                            "__type__": "Enumeration"
>                                        }
>                                    ]
>                                }
>                            ]
>                        }
>                    ]
>                },
>                {
>                    "width": 32,
>                    "local_address": 4,
>                    "name": "reg2",
>                    "descr": null,
>                    "doc": null,
>                    "uuid": "50d9b82efb5e400c81d2cd22aa16af8a",
>                    "__type__": "Register",
>                    "children": [
>                        {
>                            "slice_width": 4,
>                            "reg_offset": 4,
>                            "field_offset": 3,
>                            "name": "bf2_ref",
>                            "descr": null,
>                            "doc": null,
>                            "uuid": "cd572013939f427da02d4003fd3a2ffd",
>                            "__type__": "BitFieldRef",
>                            "children": [
>                                {
>                                    "width": 20,
>                                    "reset": 74565,
>                                    "access": "RW",
>                                    "name": "bf1",
>                                    "descr": null,
>                                    "doc": null,
>                                    "uuid": "884cc624b8c949af9c95f1b0a749c4de",
>                                    "__type__": "BitField",
>                                    "children": [
>                                        {
>                                            "value": 20,
>                                            "name": "use_auto_inc",
>                                            "descr": null,
>                                            "doc": null,
>                                            "uuid": "d4042bec7cff443781d9281931bfa791",
>                                            "__type__": "Enumeration"
>                                        },
>                                        {
>                                            "value": 10,
>                                            "name": "use_auto_dec",
>                                            "descr": null,
>                                            "doc": null,
>                                            "uuid": "25b9f2e954d244b8a8ea09523f271afd",
>                                            "__type__": "Enumeration"
>                                        }
>                                    ]
>                                }
>                            ]
>                        }
>                    ]
>                },
>                {
>                    "__ref__": "50d9b82efb5e400c81d2cd22aa16af8a"
>                }
>            ]
>        }
>    ]
>}

The `__ref__` item in the JSON output indicates that it's a reference copy of
another object with the supplied UUID.





Notes
-----

1. the _nb_attrs class attribute is used to control what is serialized in each
   class instance.


