
.. |br| raw:: html

   <br /><br />


**************
Workflow steps
**************

Preprocessing contains three main stages: preflagger, flagger, and averaging. *Preflagger* is the stage where the RFI masks
 (e.g. channels known to be prone to RFI because of a known radio source) are applied. RFI *flagging* can be done by one of the flaggers 
 existing in DP3. In the preprocessing pipeline, we have deployed AOFlagger as the more commonly used flagger. However, it can be replaced 
 with the other flagger existing in the preprocessing pipeline (MAD) or possibly a customised flagger. *Averaging* is performed to reduce 
 the size of data without losing the useful information and reducing the unhelpful fluctuations in the data. Averaging can be done in time and/or 
 frequency directions.

More information about the steps of the workflow can be found in:
https://confluence.skatelescope.org/pages/viewpage.action?pageId=205798710

Execution
--------- 

To run the pipeline from the src directory, run the following command:

  .. code-block:: bash

python3 pipeline.py --msloc your_MeasurementSet --maskloc your_RFI_mask_pickle_file.pickle --paramsloc your_parameters.json 
   

where ``--msloc`` is the location of ``your_MeasurementSet``, ``--maskloc`` is the location of ``your_RFI_mask_pickle_file``, and 
``--paramsloc`` is the location of ``your_parameters`` to identify which DP3 parameters you would like to use for each step. The parameters
should be provided through a JSON file. Here is an example of the contents in such a file. 

.. code-block:: bash

   {
     "preflagger": [
        {
        }
     ],  
     "aoflagger": [
         {
            "autocorr" : "True"
         }
     ],
     "averaging": [
         {
            "freqstep": 8,
            "timestep": 2
         }
     ]
}

The parameters' names are the same as in DP3. For example, ``freqstep`` is the number of channels to be averaged together. 



