******************
Installation guide
******************

External libraries required are:
  .. code-block:: bash

     DP3
     Casacore

Please note that currently all the packages required for the DP3 (and the DP3 itself) should be built from source against the same version of casacore.
More instructions can be found in:
https://confluence.skatelescope.org/display/SE/Cookbook+for+building+astronomical+packages+from+source 

Please also note that for the DP3 to be importable in python, the following variable should be set:

  .. code-block:: bash

     export PYTHONPATH="/home/your_home/where_you_installed_dp3_and_others/lib/python3.8/site-packages:$PYTHONPATH"      

Uninstalling
------------

It can be simply deleted.

