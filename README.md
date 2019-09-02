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
++++++++++++++++++++++++

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

Simple Iteration
++++++++++++++++

Iteration is supported by the base Node class and hence provided by all
subclasses.

For example:

    for reg in reg_map:
        for bf_ref in reg:
            print(f"bitfield reference: {bf_ref.name} has value: {bf_ref.value}")

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

Notes
-----

1. the _nb_attrs class attribute is used to control what is serialized in each
   class instance.


