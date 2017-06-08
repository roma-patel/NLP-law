NLP-law: 
 This repository contains data from USCode-Cornell website and scripts and sample code for retrieving and analysing it.
 
 # PICO-annotations


## Folders
* By PICO element:
  * Participants: `pico_pilot*`, `mesh_pilot*`, `batch5k*`
  * Interventions: `interventions_pilot*`, `interventions_batch5k*`
  * Outcomes: `outcomes_pilot*`, `outcomes_batch5k*`
* Datasets:
  * Pilot: the `pico_pilot` dataset consists of the initial pilot data; `mesh_pilot` is the initial pilot data from Ben's mesh datset. They are separated for participants but later merged into `*_pilot`.
  * Batch5k: `*_batch5k` is the same 5k-doc dataset for the main annotation.
* MTurk result files are in the corresponding `*_results` folders.

## Files
* Within data folders:
  * Structured as randomly named subfolders with 3 abstracts within each folder (3 docs per HIT).
  * `*.txt`: raw text abstracts
  * `*.ann`: raw Brat annotation files; named as `<abstract_id>.<guid>.ann`
  * `*.conf`: Brat config files
* Within `*_results` folders:
  * `*.csv`: input to MTurk. Each link corresponds to the first abstract in a data subfolder which will be the location of the HIT.
  * `*.success`: hitids and hittypeids corresponding to each line in the `*.csv` file.
  * `*.results`: MTurk results file. The `Answer.brat_link` fields correspond to the links from the input `*.csv` files; the `Answer.serveycode` fields correspond to the `guid` fields in data folders. Note that a corresponding `.ann` file cannot always be found (Brat glitch, spammers, etc).
  * `*_internal201.*` files are internal Sandbox annotations from medical students.

## Notes
* During initial development we had a more primitive MTurk format for `pico_pilot`. The results are in `template2_results.csv`, in which MTurk gave slightly different naming conventions from the `*.results` files so make sure to process that separately.
* Please ignore other files, e.g., `*_internal100.*`, `*.internal.*`, `*.old`, unless especially mentioned above.
