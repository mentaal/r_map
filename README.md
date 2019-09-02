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


