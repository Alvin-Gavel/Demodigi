"""
This is the script used for the data analysis in the paper [title goes here], authored by [author list goes here]
"""

import datetime


import preprocessing as pp
import extra_functions as ef

plotpath = 'Resultat/Artikel/Plottar'
individualplotpath = 'Resultat/Artikel/Plottar/Individer'
individualresultpath = 'Resultat/Artikel/Individer'
ef.make_folder(plotpath)
ef.make_folder(individualplotpath)
ef.make_folder(individualresultpath)

fullresultpath = 'Resultat/Artikel/Samlade_resultat.csv'
idpath = 'Resultat/Artikel/IDn.json'
manipulationpath = 'Resultat/Artikel/Manipulationer.json'

competencies = {'All':['Backup', 'WFH_Safety', 'Phishing_EmailAddresses', 'SafeEnvironments', 'Incognito', 'Spam', 'InfoOverPhone', 'GDPR_PersonalInformation', 'Cookies', 'PublicComputers', 'Virus', 'GDPR_Rights', 'Ransomware', 'IMEI', 'TwoFactorAuthentication', 'Password', 'PortableDeviceSafety', 'GDPR_SensitivePersonalData', 'PhoneFraud', 'SocialMedia', 'InfoOverInternet', 'Phishing_WebAddresses', 'OpenNetworks', 'Phishing_ShadyMails', 'GDPR_General']}

mod = pp.learning_module(competencies, n_sessions = 2, final_test = True, start_date = datetime.date.fromisoformat('2022-11-01'), end_date = datetime.date.fromisoformat('2023-01-12'))

# We read the datashop file to get the participants' results.
mod.import_raw_analytics({'QBL': 'Actual_results/2023-01-28/QBL/raw_analytics.tsv', 'pQBL': 'Actual_results/2023-01-28/pQBL/raw_analytics.tsv'})

# We expected to never need to use this method, but it looks like we have to
mod.infer_participants_from_full_results()

mod.read_participants_results(database = 'raw_analytics')

mod.describe_module()
results = mod.describe_performance()

mod.plot_initial_performance(plotpath)
mod.plot_results(plotpath, individualplotpath)

mod.export_full_results(fullresultpath)
mod.export_individual_results(individualresultpath)
mod.export_IDs(idpath, drop_unfinished = True)
mod.export_single_manipulation(manipulationpath, 'pQBL', drop_unfinished = True)
