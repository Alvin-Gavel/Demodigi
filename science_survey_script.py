"""
This is a script that analyses the results of the survey in the learning module
IT-säkerhet. This analysis is so different from everything else that we do that
it does not use any of the already existing modules.
"""

import re
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

datasets = {'QBL': pd.read_csv('Utilities/Actual_results/2023-01-28/QBL/raw_analytics.tsv', sep='\t'),
'pQBL':pd.read_csv('Utilities/Actual_results/2023-01-28/pQBL/raw_analytics.tsv', sep='\t')}

# This holds the participants that actually finished the module.
ID_path = 'Utilities/Resultat/Artikel/IDn.json'
f = open(ID_path, 'r')
packed = f.read()
f.close()
unpacked = json.loads(packed)
all_ids = set(map(int, set(unpacked['IDs'])))

# List the members of each version of the learning module who actually finished the module
members = {}
n_members = {}
for dataset_name, dataset in datasets.items():
   members[dataset_name] = list(set(dataset['Student ID']).intersection(all_ids))
   n_members[dataset_name] = len(members[dataset_name])

question_sets = {
'One to five scale': {'Survey_UnderstoodInstructions': 'I understood the instructions',
                      'Survey_LikeInternetbasedLearning': 'I like internet-based learning',
                      'Survey_ILearnedALot': 'The course was informative',
                      'Survey_GoodLevelOfDifficulty': 'The questions were of appropriate difficulty',
                      'Survey_LikedTheFeedback': 'The feedback in the questions was helpful',
                      'Survey_QBLLearning': 'The fact that the course was question-based helped me learn the material',
                      'Survey_QBLMotivation': 'The fact that the course was question-based motivated me',
                      'Survey_MoreQBLCourses': 'If I take an online course in the future, I hope it is question-based'},
'Never to always scale': {'Survey_SearchingForAnswers': 'I looked for the correct answer (e.g. on the internet) before answering the questions',
                          'Survey_FirstTry': 'I tried my best to answer the questions correctly on the first try',
                          'Survey_ContinuedToRespond': 'After answering a question correctly, I continued to click on incorrect answers to get more feedback',
                          'Survey_Frustration': 'How often did you feel frustrated during the course?'}
}


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
   for question_name, question_text in question_set.items():
      responses[question_name] = {}
      errors[question_name] = {}
      for dataset_name, dataset in datasets.items():
         entries = dataset[(dataset['Activity Title'] == question_name) & (dataset['Student ID'].isin(all_ids))]
      
         responses[question_name][dataset_name] = np.zeros(5)
         for response in entries['Feedback']:
            match = response_regex.findall(response)
         
            if len(match) == 1:
               digit = int(digit_regex.findall(match[0])[0])
               responses[question_name][dataset_name][digit - 1] += 1
      
         errors[question_name][dataset_name] = np.sqrt(responses[question_name][dataset_name]) / n_members[dataset_name]
         responses[question_name][dataset_name] /= n_members[dataset_name]

      plt.clf()
      x_qbl = np.arange(1, 6) - 0.20
      plt.bar(x_qbl, responses[question_name]['QBL'], width = 0.4, label = 'QBL')
      plt.errorbar(x_qbl, responses[question_name]['QBL'], yerr=errors[question_name]['QBL'], fmt='none', ecolor='k', capsize = 5)
      x_pqbl = np.arange(1, 6) + 0.20
      plt.bar(x_pqbl, responses[question_name]['pQBL'], width = 0.4, label = 'pQBL')
      plt.errorbar(x_pqbl, responses[question_name]['pQBL'], yerr=errors[question_name]['pQBL'], fmt='none', ecolor='k', capsize = 5)
      plt.ylabel('Frequency')
      #plt.title(question_text)
      plt.legend()
      if question_set_name == 'Never to always scale':
         plt.xticks(ticks = np.arange(1, 6), labels = ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'], rotation=90)
      
      plt.tight_layout()
      plt.savefig('Article_plots/Responses_{}.png'.format(question_name))

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
   entries = dataset[(dataset['Activity Title'] == 'Survey_TimeOnCourse') & (dataset['Student ID'].isin(all_ids))]

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
plt.savefig('Article_plots/Times_own_estimate.png')
