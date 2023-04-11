"""
This is a script that uses the Python module factorial_experiment to
read the results from the course module IT-säkerhet, which must
in turn be created with the script PP_science_script in the
directory Utilities.
"""

import factorial_experiment as fe

skills = ['Backup', 'WFH_Safety', 'Phishing_EmailAddresses', 'SafeEnvironments', 'Incognito', 'Spam', 'InfoOverPhone', 'GDPR_PersonalInformation', 'Cookies', 'PublicComputers', 'Virus', 'GDPR_Rights', 'Ransomware', 'IMEI', 'TwoFactorAuthentication', 'Password', 'PortableDeviceSafety', 'GDPR_SensitivePersonalData', 'PhoneFraud', 'SocialMedia', 'InfoOverInternet', 'Phishing_WebAddresses', 'OpenNetworks', 'Phishing_ShadyMails', 'GDPR_General']

bound = fe.boundaries(0.5, 0.8, 0.1)

mod = fe.real_learning_module(len(skills), 2, 'Utilities/Resultat/Artikel/IDn.json', 'Utilities/Resultat/Artikel/Individer', manipulation_path = 'Utilities/Resultat/Artikel/Manipulationer.json', boundaries = bound)
trial_study = fe.study('Artikel', mod, plot_folder = 'Article_plots')
trial_study.describe()
trial_study.do_tests()
trial_study.summarise_results()
trial_study.plot_results()


print('For comparison_testing with bounds 0.6')
comparison_bound = fe.boundaries(0.6, 0.6, 0.1)

mod = fe.real_learning_module(len(skills), 2, 'Utilities/Resultat/Artikel/IDn.json', 'Utilities/Resultat/Artikel/Individer', manipulation_path = 'Utilities/Resultat/Artikel/Manipulationer.json', boundaries = comparison_bound)
trial_study = fe.study('Artikel', mod, plot_folder = 'Article_plots/60_percent')
trial_study.describe()
trial_study.do_tests()
trial_study.summarise_results()
trial_study.plot_results()


print('For comparison_testing with bounds 0.7')
comparison_bound = fe.boundaries(0.7, 0.7, 0.1)

mod = fe.real_learning_module(len(skills), 2, 'Utilities/Resultat/Artikel/IDn.json', 'Utilities/Resultat/Artikel/Individer', manipulation_path = 'Utilities/Resultat/Artikel/Manipulationer.json', boundaries = comparison_bound)
trial_study = fe.study('Artikel', mod, plot_folder = 'Article_plots/70_percent')
trial_study.describe()
trial_study.do_tests()
trial_study.summarise_results()
trial_study.plot_results()


print('For comparison_testing with bounds 0.8')
comparison_bound = fe.boundaries(0.8, 0.8, 0.1)

mod = fe.real_learning_module(len(skills), 2, 'Utilities/Resultat/Artikel/IDn.json', 'Utilities/Resultat/Artikel/Individer', manipulation_path = 'Utilities/Resultat/Artikel/Manipulationer.json', boundaries = comparison_bound)
trial_study = fe.study('Artikel', mod, plot_folder = 'Article_plots/80_percent')
trial_study.describe()
trial_study.do_tests()
trial_study.summarise_results()
trial_study.plot_results()
