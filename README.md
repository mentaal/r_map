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

Nice to haves
-------------

block.reg.write(bf=10) #a register write only setting bf to 10
It would be trivial to tack on a writer function/object to handle register
writes. Best left out this implementation r_map is intended to be sim

block.reg.bf=10        # a read mod write setting the bf to 10
problem with this is ambiguity. What if a sub field's name clashed with a node's
method or attributes?
Answer to this:
Most methods are prepended with a '_'


Notes
-----

1. the _nb_attrs class attribute is used to control what is serialized in each
   class instance.


