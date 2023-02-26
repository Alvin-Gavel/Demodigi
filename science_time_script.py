"""
This is a script that tries to estimate the amount of time participants spent
on the learning module IT-säkerhet. This analysis is so different from
everything else that we do that it does not use any of the already existing
modules.
"""

import datetime

import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt

# This is the maximum amount of time that we believe a person will actually
# spend on answering a question. If we see that somebody takes more time than
# that between two subsequent questions, we assume that they actually went on a
# coffee break or something and insert a dummy time instead.
#
# Note that this assumed time is a fairly important assumption, and the validity
# of our analysis depends on it being reasonable.
max_time = datetime.timedelta(minutes=5)


datasets = {'QBL': pd.read_csv('Utilities/Actual_results/2023-01-28/QBL/raw_analytics.tsv', sep='\t'),
'pQBL':pd.read_csv('Utilities/Actual_results/2023-01-28/pQBL/raw_analytics.tsv', sep='\t')}

for dataset in datasets.values():
   dataset['Date Created']= pd.to_datetime(dataset['Date Created'])

# TODO: Replace this with something that reads only the participants who finished.
members = {}
for dataset_name, dataset in datasets.items():
   members[dataset_name] = list(set(dataset['Student ID']))

skills = ['Backup', 'WFH_Safety', 'Phishing_EmailAddresses', 'SafeEnvironments', 'Incognito', 'Spam', 'InfoOverPhone', 'GDPR_PersonalInformation', 'Cookies', 'PublicComputers', 'Virus', 'GDPR_Rights', 'Ransomware', 'IMEI', 'TwoFactorAuthentication', 'Password', 'PortableDeviceSafety', 'GDPR_SensitivePersonalData', 'PhoneFraud', 'SocialMedia', 'InfoOverInternet', 'Phishing_WebAddresses', 'OpenNetworks', 'Phishing_ShadyMails', 'GDPR_General']


timestamps = {}
for dataset_name, dataset in datasets.items():
   for member in members[dataset_name]:
      for skill in skills:
         timestamps[member] = sorted(dataset.loc[dataset['Student ID'] == member]['Date Created'])
         
total_time = {}
assumed_coffee_breaks = {}
for member_name, member_timestamps in timestamps.items():
   total_time[member_name] = datetime.timedelta(minutes=0)
   assumed_coffee_breaks[member_name] = 0
   for i in range(len(member_timestamps) - 1):
      this_answer = member_timestamps[i]
      next_answer = member_timestamps[i + 1]
      time_diff = next_answer - this_answer
      if time_diff > max_time:
         total_time[member_name] += max_time
         assumed_coffee_breaks[member_name] += 1
      else:
      	 total_time[member_name] += time_diff
