.. note::

   Since we loaded the ``wdmapp`` module via Spack the binaries are in your ``PATH``
   and their location can be retrieved with the ``which xgc-es gene cpl``
   command.

Run the effis pre-processor:

.. code-block:: sh

  $ effis-compose.py run_1.yaml

Submit the job:

.. code-block:: sh

  $ effis-submit /path/to/testDir
