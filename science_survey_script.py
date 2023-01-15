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

n_members = {}
for dataset_name, dataset in datasets.items():
   n_members[dataset_name] = len(set(dataset['Student ID']))


one_to_five_questions = ['Survey_UnderstoodInstructions', 'Survey_LikeInternetbasedLearning', 'Survey_ILearnedALot', 'Survey_GoodLevelOfDifficulty', 'Survey_LikedTheFeedback', 'Survey_QBLLearning', 'Survey_QBLMotivation', 'Survey_MoreQBLCourses']

# To clarify what goes on here: There is no column in the data from OLI Torus that
# actually tells us what answer a user has given. Instead, we go digging in the column
# named feedback, where entries typically look something like this:
# {"content":[{"children":[{"text":"4"}],"id":"4096322134","type":"p"}],"id":"2655357029"}
# We then pick out the string immediately after "text":

response_regex = re.compile('"text":"[1-5]"')
digit_regex =  re.compile('[1-5]')

responses = {}
errors = {}
for question in one_to_five_questions:
   responses[question] = {}
   errors[question] = {}
   for dataset_name, dataset in datasets.items():
      entries = dataset[dataset['Activity Title'] == question]
      
      responses[question][dataset_name] = np.zeros(5)
      for response in entries['Feedback']:
         match = response_regex.findall(response)
         
         if len(match) == 1:
            digit = int(digit_regex.findall(match[0])[0])
            responses[question][dataset_name][digit - 1] += 1
      
      errors[question][dataset_name] = np.sqrt(responses[question][dataset_name]) / n_members[dataset_name]
      responses[question][dataset_name] /= n_members[dataset_name]

   plt.clf()
   x_qbl = np.arange(1, 6) - 0.20
   plt.bar(x_qbl, responses[question]['QBL'], width = 0.4)
   plt.errorbar(x_qbl, responses[question]['QBL'], yerr=errors[question]['QBL'], fmt='none', ecolor='k', capsize = 5)
   x_pqbl = np.arange(1, 6) + 0.20
   plt.bar(x_pqbl, responses[question]['pQBL'], width = 0.4)
   plt.errorbar(x_pqbl, responses[question]['pQBL'], yerr=errors[question]['pQBL'], fmt='none', ecolor='k', capsize = 5)
   plt.ylabel('Responses')
   plt.title(question)
   plt.tight_layout()
   plt.savefig('Article_plots/Responses_{}.png'.format(question))
