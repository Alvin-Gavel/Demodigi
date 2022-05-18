"""
This module was written for the ESF-financed project Demokratisk
Digitalisering. The project is a collaboration between
Arbetsförmedlingen (AF) and Kungliga Tekniska Högskolan (KTH). The
purpose of the project is to increase the digital competence - as
defined at https://ec.europa.eu/jrc/en/digcomp - of people working at
Arbetsförmedlingen, and by extension also job seekers. This will be
done by learning modules at KTH using OLI-Torus.

--- About this Python module ---

This module is intended to read the tsv-files that come out of OLI-
TORUS, and transform them into json files that contain only the
information used by the factorial_experiment module. It is mostly
intended as a proof-of-concept. I intend to eventually work the
contents into the factorial_experiment module.

Written by Alvin Gavel,

https://github.com/Alvin-Gavel/Demodigi
"""

import numpy as np
import pandas as pd
   
class participant:
   """
   This represents a single person taking a learning module.
   
   Attributes
   ----------
   ID : string
   \tSome unique identifier of the participant. For privacy reasons, this
   \tis unlikely to be their actual name.
   """
   def __init__(self, ID):
      self.ID = ID
      self.results = {}
      return
   
class learning_module:
   """
   This represents one learning module in the project.
  
   Attributes
   ----------
   questions : list of string
   \tA list of the questions given in the learning module, as identified
   \tin the "Activity Title" column in the output from OLI-Torus
   participants : list of participant
   \tA list of the people taking the learning module, as identified in the
   \t"Student ID" column in the output from OLI-Torus
   """
   def __init__(self, questions, participants):
      self.questions = questions
      self.participants = participants
      self.full_results = None
      self.results_read = False
      return
      
   def import_oli_results(self, filepath):
      """
      Import a file with the raw statistics directly out of OLI-Torus, in the
      tab-separated values format.
      """
      self.full_results = pd.read_csv(filepath, sep='\t')
      self.results_read = True
      return
   
   def read_participant_results(self, participant):
      """
      Find out, for each question, how many tries the participant needed to 
      answer it correctly.
      """
      if not self.results_read:
         print('No results to read!')
         return
      correct_participant = self.full_results[self.full_results['Student ID'] == participant.ID]
      for question in self.questions:
         correct_question = correct_participant[correct_participant['Activity Title'] == question]
         try:
            index_first_correct = correct_question["Correct?"].eq(True).idxmax()
            n_tries = correct_question["Attempt Number"][index_first_correct]
         except ValueError:
            n_tries = np.inf
         participant.results[question] = n_tries
      return