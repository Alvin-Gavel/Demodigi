"""
This is the script used for the data analysis in the paper [title goes here], authored by [author list goes here]
"""

import preprocessing as pp
import extra_functions as ef

plotpath = 'Resultat/Artikel/Plottar'
fullresultpath = 'Resultat/Artikel/Samlade_resultat.csv'
individualresultpath = 'Resultat/Artikel/Individer'

ef.make_folder(plotpath)
ef.make_folder(fullresultpath)
ef.make_folder(individualresultpath)

# We start by looking at how the individual competencies develop over time, as we had originally planned to do
competencies = {'Misc':['Backup', 'Cookies', 'IMEI', 'Incognito', 'InfoOverInternet', 'InfoOverPhone', 'MacroVirus', 'OpenNetworks', 'Password', 'PasswordManager', 'PhoneFraud', 'PortableDeviceSafety', 'PublicComputers', 'PUK', 'Ransomware', 'SafeEnvironments', 'SocialMedia', 'Spam', 'TwoFactorAuthentication', 'Virus', 'WFH_Safety'],
'Phishing':['Phishing_EmailAddresses', 'Phishing_ShadyMails', 'Phishing_WebAddresses'],
'GDPR':['GDPR_General', 'GDPR_PersonalInformation', 'GDPR_Rights', 'GDPR_SensitivePersonalData']}

mod = pp.learning_module(competencies, n_sessions = 4, section_slug = 'itskerhet_demokratisk_digitali_31cr5')

# We read the datashop file to get the participants' results.
mod.import_raw_analytics(['Actual_results/2022-12-11/Datshop and Raw_QBL/raw_analytics.tsv', 'Actual_results/2022-12-11/Datashop and Raw_no_QBL/raw_analytics.tsv'])

# We expected to never need to use this method, but it looks like we have to
mod.infer_participants_from_full_results()

mod.read_participants_results(database = 'raw_analytics')

mod.plot_initial_performance(plotpath)
mod.export_full_results(fullresultpath)
mod.export_individual_results(individualresultpath)
