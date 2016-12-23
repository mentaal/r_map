r_map
=====

A library for working with register map data.
The data source is abstracted such that if a user wants to work with a
particular data source, he/she may:

1. Provide an appropriately formatted serialized data source (probably the
   easiest)
2. Create a parser of the source data and dynamically generate the data
   structure using the provided data classes

Nice to haves
-------------


block.reg.write(bf=10) #a register write only setting bf to 10
block.reg.bf=10        # a read mod write setting the bf to 10
problem with this is ambiguity. What if a sub field's name clashed with a node's
method or attributes?


Notes
-----

1. the _nb_attrs class attribute is used to control what is serialized in each
   class instance.


