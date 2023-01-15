"""
This is a script that analyses the results of the survey in the learning module
IT-säkerhet. This analysis is so different from everything else that we do that
it does not use any of the already existing modules.
"""

import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datasets = {'QBL': pd.read_csv('Utilities/Actual_results/2022-12-11/Datshop and Raw_QBL/raw_analytics.tsv', sep='\t'),
'pQBL':pd.read_csv('Utilities/Actual_results/2022-12-11/Datashop and Raw_no_QBL/raw_analytics.tsv', sep='\t')}

one_to_five_questions = ['Survey_UnderstoodInstructions', 'Survey_LikeInternetbasedLearning', 'Survey_ILearnedALot', 'Survey_GoodLevelOfDifficulty', 'Survey_LikedTheFeedback', 'Survey_QBLLearning', 'Survey_QBLMotivation', 'Survey_MoreQBLCourses']

# To clarify what goes on here: There is no column in the data from OLI Torus that
# actually tells us what answer a user has given. Instead, we go digging in the column
# named feedback, where entries typically look something like this:
# {"content":[{"children":[{"text":"4"}],"id":"4096322134","type":"p"}],"id":"2655357029"}
# We then pick out the string immediately after "text":

response_regex = re.compile('"text":"[1-5]"')
digit_regex =  re.compile('[1-5]')

responses = {}
for question in one_to_five_questions:
   responses[question] = {}
   for dataset_name, dataset in datasets.items():
      responses[question][dataset_name] = []
      entries = dataset[dataset['Activity Title'] == question]
      for response in entries['Feedback']:
         match = response_regex.findall(response)
         if len(match) == 1:
            digit = int(digit_regex.findall(match[0])[0])
            responses[question][dataset_name].append(digit)
      
      plt.clf()
      plt.hist(responses[question][dataset_name])
      plt.ylabel('Responses')
      plt.title(question)
      plt.tight_layout()
      plt.savefig('Article_plots/Responses_{}_{}.png'.format(question, dataset_name))
