
.. |br| raw:: html

   <br /><br />


**************
Workflow steps
**************

This workflow/pipeline uses DP3 library. Currently only aoflagger works. Preflagger and averaging will be astivated soon.

More information about the steps of the workflow can be found in:
https://confluence.skatelescope.org/pages/viewpage.action?pageId=205798710

Execution
--------- 

To run the pipeline from the src directory, run the following command:

  .. code-block:: bash

     python3 pipeline.py --msloc your_MeasurementSet --maskloc your_RFI_mask_pickle_file.pickle

 

