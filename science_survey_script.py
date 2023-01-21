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

question_sets = {'One to five scale': ['Survey_UnderstoodInstructions', 'Survey_LikeInternetbasedLearning', 'Survey_ILearnedALot', 'Survey_GoodLevelOfDifficulty', 'Survey_LikedTheFeedback', 'Survey_QBLLearning', 'Survey_QBLMotivation', 'Survey_MoreQBLCourses'],
'Never to always scale': ['Survey_SearchingForAnswers', 'Survey_FirstTry', 'Survey_ContinuedToRespond', 'Survey_Frustration']}


# To clarify what goes on here: There is no column in the data from OLI Torus that
# actually tells us what answer a user has given. Instead, we go digging in the column
# named feedback, where entries typically look something like this:
# {"content":[{"children":[{"text":"4"}],"id":"4096322134","type":"p"}],"id":"2655357029"}
# We then pick out the string immediately after "text":

response_regex = re.compile('"text":"[1-5]"')
digit_regex = re.compile('[1-5]')

responses = {}
errors = {}
for question_set_name, question_set in question_sets.items():
   for question in question_set:
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
      plt.bar(x_qbl, responses[question]['QBL'], width = 0.4, label = 'QBL')
      plt.errorbar(x_qbl, responses[question]['QBL'], yerr=errors[question]['QBL'], fmt='none', ecolor='k', capsize = 5)
      x_pqbl = np.arange(1, 6) + 0.20
      plt.bar(x_pqbl, responses[question]['pQBL'], width = 0.4, label = 'pQBL')
      plt.errorbar(x_pqbl, responses[question]['pQBL'], yerr=errors[question]['pQBL'], fmt='none', ecolor='k', capsize = 5)
      plt.ylabel('Frequency')
      plt.title(question)
      plt.legend()
      if question_set_name == 'Never to always scale':
         plt.xticks(ticks = np.arange(1, 6), labels = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'], rotation=90)
      
      plt.tight_layout()
      plt.savefig('Article_plots/Responses_{}.png'.format(question))

# Here we look for the time input by the users. This requires us to dig in the
# Student Response column, where entries typically look something like this:
# {"files":[],"input":"25"}

time_regex = re.compile('"input":"[0-9]+"')
number_regex = re.compile('[0-9]+')

times = {}
binned_times = {}
errors = {}
bin_edges = [0, 15, 45, 75, 105, 135, 165, 195, 225, 255]
n_edges = len(bin_edges)
for dataset_name, dataset in datasets.items():
   entries = dataset[dataset['Activity Title'] == 'Survey_TimeOnCourse']

   times[dataset_name] = []
   for response in entries['Student Response']:
      match = time_regex.findall(response)
         
      if len(match) == 1:
         number = int(number_regex.findall(match[0])[0])
         times[dataset_name].append(number)

   binned_times[dataset_name] = np.histogram(times[dataset_name], bins=bin_edges)
   errors[dataset_name] = np.sqrt(binned_times[dataset_name][0])

   print('{} took on average {} minutes'.format(dataset_name, np.median(times[dataset_name])))

plt.clf()
x_qbl = np.arange(1, n_edges) - 0.20
plt.bar(x_qbl, binned_times['QBL'][0], width = 0.4, label = 'QBL')
plt.errorbar(x_qbl, binned_times['QBL'][0], yerr=errors['QBL'], fmt='none', ecolor='k', capsize = 3)
x_pqbl = np.arange(1, n_edges) + 0.20
plt.bar(x_pqbl, binned_times['pQBL'][0], width = 0.4, label = 'pQBL')
plt.errorbar(x_pqbl, binned_times['pQBL'][0], yerr=errors['pQBL'], fmt='none', ecolor='k', capsize = 3)

plt.xticks(ticks = np.arange(0, n_edges), labels = bin_edges)
plt.ylabel('Responses')
plt.xlabel('Time spent on course [min]')
plt.legend()
plt.tight_layout()
plt.savefig('Article_plots/Times.png')
