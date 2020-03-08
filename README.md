# r_map

A library for working with register map data.
The data source is abstracted such that if a user wants to work with a
particular data source, he/she may:

1. Provide an appropriately formatted serialized data source (probably the
   easiest)
2. Create a parser of the source data and dynamically generate the data
   structure using the provided data classes

## Purpose

1. Easily utilize register map data
2. Be able to iterate through register map from arbitrary position
3. Provide conveniences for walking through data
4. Provide ability to serialize/deserialize data
5. Provide mechanism to easily subclass base element implementations
6. Provide means to register which elements are accessed in data base and create
   a subtree from this data

## Features

### Key and attribute access

Key and attribute access to an elements sub elements. The key access is
particularly useful for cases where a sub element happens to have the name of a
reserved keyword in Python.

```python
    r_map1.reg.value = 10
    r_map1['reg'].value = 10
```

That elements are not intended to be added to a node via key based assignment
like a dictionary. A method: `_add` is provided for that.

Key based assignment is not intended to be supported because it can result in a
sub element having an alias which would be confusing and is an unlikely usecase.

### Simple Iteration

Iteration is supported by the base Node class and hence provided by all
subclasses.

For example:

```python

    for reg in reg_map:
        for bf_ref in reg:
            print(f"bitfield reference: {bf_ref.name} has value: {bf_ref.value}")
```

### Register to bitfield value mapping

A register's value is based on its component bitfield's values. In fact, there
is an additional layer of indirection to support a register only having a
partial view to a bitfield. It's therefore possible for multiple registers to
have access to the same bitfield. Support for this level is complexity is baked
into the data structre and modelled with a class: BitFieldRef.

A full register map tree is serialized using a common dictionary with nodes
referencing others via their uuids.

For example:

    "1b99635555e647638f8a1ff38a1e3cf1": {
        "name": "root",
        "type": "Node",
        "children": [
            "3e2f9ba277e44050b52b5111fd814008"
        ]
    },
    "3e2f9ba277e44050b52b5111fd814008": {
        "name": "r_map1",
        "descr": "An example register map containing r
        "local_address": 268435456,
        "type": "RegisterMap",
        "children": [
            "c897cf71021449bdbdc819e7255fcab7",
            "569715f765f14ba09313796ee98b6db6"
        ]
    },
    "c897cf71021449bdbdc819e7255fcab7": {
        "local_address": 0,
        "name": "reg1",
        "width": 32,
        "type": "Register",
        "children": [
            "8cded8916e014bb3ab621e327f9c0ae8"
        ]
    },
    "8cded8916e014bb3ab621e327f9c0ae8": {
        "reg_offset": 8,
        "field_offset": 7,
        "name": "bf1_ref",
        "slice_width": 6,
        "type": "BitFieldRef",
        "children": [
            "b138d3d5335442479f25ec4d57859cda"
        ]
    },
    "b138d3d5335442479f25ec4d57859cda": {
        "access": "RW",
        "name": "bf1",
        "reset_val": 74565,
        "width": 20,
        "doc": "Some documentation to describe the bit
        "type": "BitField",
        "children": [
            "ba75ebd0924a46f29f0dd1726fd5fb5f",
            "36b5d3a221e6400bba2d76a303dac2c2"
        ]
    },
    "ba75ebd0924a46f29f0dd1726fd5fb5f": {
        "name": "use_auto_inc",
        "value": 20,
        "type": "Enumeration"
    },
    "36b5d3a221e6400bba2d76a303dac2c2": {
        "name": "use_auto_dec",
        "value": 10,
        "type": "Enumeration"
    },
    "569715f765f14ba09313796ee98b6db6": {
        "local_address": 4,
        "name": "reg2",
        "width": 32,
        "type": "Register",
        "children": [
            "14b8d11fea244200a6d0efee16d740f7",
            "37a9c221ab77446aafe9f74ec14c78c6",
            "6f695b3dbdd74cb3abaddf82c9594e4b"
        ]
    },
    "14b8d11fea244200a6d0efee16d740f7": {
        "_alias": true,
        "reg_offset": 0,
        "field_offset": 0,
        "name": "bf4_ref",
        "slice_width": 2,
        "_ref": "6f695b3dbdd74cb3abaddf82c9594e4b",
        "type": "BitFieldRef"
    },
    "6f695b3dbdd74cb3abaddf82c9594e4b": {
        "reg_offset": 5,
        "field_offset": 2,
        "name": "bf3_ref",
        "slice_width": 5,
        "type": "BitFieldRef",
        "children": [
            "28c6a9c6929a4ad2baabc18751ec21d3"
        ]
    },
    "28c6a9c6929a4ad2baabc18751ec21d3": {
        "access": "R",
        "name": "bf2",
        "reset_val": 26505,
        "width": 20,
        "type": "BitField"
    },
    "37a9c221ab77446aafe9f74ec14c78c6": {
        "_alias": true,
        "reg_offset": 4,
        "field_offset": 3,
        "name": "bf2_ref",
        "slice_width": 4,
        "_ref": "8cded8916e014bb3ab621e327f9c0ae8",
        "type": "BitFieldRef"
    },
    "root": "1b99635555e647638f8a1ff38a1e3cf1"
}

The `_ref` attribute facilitates modeling that one node can be an instance of
another. Which saves duplication of common information within the serialized
tree. The `_alias` attribute indicates that an instance can be an alias of
another. This simply means that the new instance's bitfields will be shared with
the source node.

## r_map classes

### Common Attributes

All tree objects have the following common attributes:

1. name
   The name of the item
2. descr
   A short description of the item
3. doc
   A longer description of the item

Note that the descr and doc attributes could potentially be None or an empty
string.

There are other common attributes but as a user of an r_map tree, they are not
of interest.

### RegisterMap

Used to hold register objects.

RegisterMap Attributes


Objects of this class have:

1. address
   The starting address of the register map. This may not be awfully useful as
   the most interesting addresses are probably those of the child Registers.
2. local_address
   The aforementioned address is found dynamically by summing the local_address
   with the local_addresses of the parent nodes in the tree hierarchy. Unless
   you're using a subclassed FixedRegisterMap where the local_address ==
   address.

#### RegisterMap Methods

1. read
   This method can be used to read the current register map's data and update
   the child register's values. It relies upon a `_block_read_func` function
   having been added to it or some parent in the tree hierarchy.
2. write
   Write the register map's child register values value to some destination.
   Note that if there are gaps between adjacent child registers, zeroes are
   written to those addresses.
   This method relies upon a `_block_write_func` having been added.

### Register

#### Register Attributes

Objects of this class have the same attributes as RegisterMap objects and in
addition have a width attribute, indicating the width of the register.
These are children of RegisterMap instances.

Registers have the following additional attributes:
1. value
   This is the current value of the register. It is dynamically computed based
   on the current values from all of the child BitFieldRefs. It can be assigned
   directly as well and the value will update the child bitfields accordingly.
2. reset_val
   This is the reset value of the register
3. access
   This indicates the access level for the register, dynamically computed based
   on the child BitFieldRef's access levels. If different children have
   different access levels, they will be `'|'.join`ed together.

#### Register Methods

1. read
   This method can be used to read the current register's data and update the
   register's value. It relies upon a `_reg_read_func` function having been added
   to it or some parent in the tree hierarchy.
2. write
   Write the register's value to some destination. Works similarly to the read
   function above and similarly relies upon a `_reg_write_func` having been
   added.

### BitFieldRef

These ojects represent a contribution of a bitfield within a register. They
allow a register to provide access to only a portion of a bitfield.
Alternatively they also allow multiple registers to provide access to common
bitfields or for bitfields to span multiple registers.

#### BitFieldRef Attributes

Objects of this class are children of Register instances. They have the
following additional attributes:

1. reg_offset
   This is the offset within the host register that the contribution from this
   object's child bitfield starts at.
2. slice_width
   This is the width of the slice from the child bitfield that this contribution
   represents.
3. field_offset
   This is like the reg_offset but instead its the offset within the child
   bitfield that this contribution is taken from.
4. value
   This is the value of the contribution of the child's bitfield, shifted up by
   `reg_offset`
5. Represents what `value` above would be at reset time.
6. bf
   This attribute returns the child bitfield of the bitfield reference.

### BitField

### BitField Attributes

Objects of this class represent a bitfield.

They have the following additional attributes:

1. width
   The width of the bit field in bits
2. reset_val
   The value of this bit field at reset.
3. access
   The access level of the reset_val. This is currently just for documentation
   sake but could conceivably be used by the user. It would contain a string
   such as 'RW' or 'R' for example.
4. value
   This is the current value of the bitfield.

### BitField

#### BitField Methods

1. reset
   Reset the value of this bitfield to the value specified by `reset_val`.
2. annotation
   Find the name of a child annotation, should its value match the current
   value, otherwise, return the value in hex.

### Enumeration

Objects of this class are used to represent an enumeration. They are children of
BitField objects. They can be assigned directly to a BitField's value.

#### Enumeration Attributes

Enumeration objects have a value Attribute to provide the value of it.

## Notes

1. the `_nb_attrs` class attribute is used to control what is serialized in each
   class instance.


