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

Key and attribute access to an elements sub elements. The key access is
particularly useful for cases where a sub element happens to have the name of a
reserved keyword in Python.

Example ::

    r_map1.reg.value = 10
    r_map1['reg'].value = 10



Notes
-----

1. the _nb_attrs class attribute is used to control what is serialized in each
   class instance.


