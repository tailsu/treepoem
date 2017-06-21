.. :changelog:

-------
History
-------

.. Insert new release notes below this line

1.2.0 (2017-06-21)
------------------

* Add ``treepoem.barcode_types``, a set of all the names of supported barcode
  types, and error if asked to generate a barcode of an unknown type.

1.1.0 (2017-04-13)
------------------

* Support Windows.

1.0.1 (2016-03-30)
------------------

* Add the missing ``BWIPP`` files.

1.0.0 (2016-03-23)
------------------

* Use ``$PATH`` to find ``gs`` binary.
* Rename ``PostscriptError`` to ``TreepoemError``.
* Add basic ``setup.py``.
* Setup Travis CI build.
* Setup Tox
