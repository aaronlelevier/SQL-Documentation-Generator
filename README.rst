README
======

Goal
----
To walk down the directory path of a given SQL repo, and generate 
documentation in ``.rst`` format.

Explanation
-----------
- Docs will be 1 doc per DIR in the folder structure. 
- Outputs "Sub-sections" per each .sql file.  
- Only grabs documentation wrapped in /* <some_comments> */
- Dirs and sub-dirs are separated in the ``.rst`` filename by "__"

Usage
-----
.. code-block::

	python /path/to/create_docs.py <dir at start of repo. if omitted, current dir.>

Testing
-------
Requirements

- pytest

Run:

.. code-block::

	py.test /path/to/create_docs.py