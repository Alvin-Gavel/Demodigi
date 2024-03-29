This repository contains code written for the ESF-financed project _Demokratisk Digitalisering_. The project is a collaboration between Arbetsförmedlingen (AF) and Kungliga Tekniska Högskolan (KTH). The purpose of the project is to increase the digital competence - as defined at https://ec.europa.eu/jrc/en/digcomp - of people working at AF, and by extension also job seekers. This will be done by learning modules at KTH using OLI-Torus.

The current contents of the repository are:

`README.md`: This text

`requirements.txt`: File listing the Python modules used in this repository, and which versions I used.

`factorial_experiment.py`: Python module for analysing the results of a factorial experiment that we plan to do as part of the study. It can also be used for simulating similar studies, to test that the analysis at least makes sense on paper.

`FE_demonstration_script.py`: Script that demonstrates the use of the module `factorial_experiment` by implementing a simple simulated study. To make that easier, it has verbose comments explaining what happens at every step along the way.

`FE_test_script.py`: Script for testing that the module `factorial_experiment` actually works as intended.

`FE_minimal_size_script.py`: Script using the module `factorial_experiment` to try to find the minimal number of participants that we need in order to measure the effects that we are interested in.

`KL_analysis_script.py`: Script for analysing data from the learning module `Kartläggning`. The data must first be rewritten into a format readable by the `Factorial_experiment` module by the module `preprocessing`, which is found in the directory `Utilities`.

`science_analysis_script.py`: Script for analysing data for the article (name pending). The data comes from the learning module `IT-säkerhet`. The data must first be rewritten into a format readable by the `Factorial_experiment` module by the script `PP_science_script` which uses the module `preprocessing`, both in the directory `Utilities`.

`science_survey_script.py`: Script for analysing the answers to the survey given as part of the learning module `IT-säkerhet`.

`science_time_script.py`: Script for estimating the time participants spent on the learning module `IT-säkerhet`.

`behavioural_experiment.py`: Python module for simulating a behavioural experiment that we plan to do as part of the study. With time, I will also add code for analysing the results of the actual experiment.

`BE_test_script.py`: Script intended as a test of the module `behavioural_experiment`, by running some functions and plotting the results.

`Pedagogics`: Directory containing code written to demonstrate the underlying ideas behind our analysis.

`Utilities`: Directory containing code written to solve specific technical problems of no scientific interest.
