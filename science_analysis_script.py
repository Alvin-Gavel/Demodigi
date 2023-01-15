"""
This is a script that uses the Python module factorial_experiment to
read the results from the course module kartläggningsmodul, which must
in turn be created with the script PP_mapping_module_script in the
directory Utilities.
"""

import factorial_experiment as fe

skills = ['Backup', 'Cookies', 'IMEI', 'Incognito', 'InfoOverInternet', 'InfoOverPhone', 'OpenNetworks', 'Password', 'PhoneFraud', 'PortableDeviceSafety', 'PublicComputers', 'Ransomware', 'SafeEnvironments', 'SocialMedia', 'Spam', 'TwoFactorAuthentication', 'Virus', 'WFH_Safety', 'Phishing_EmailAddresses', 'Phishing_ShadyMails', 'Phishing_WebAddresses', 'GDPR_General', 'GDPR_PersonalInformation', 'GDPR_Rights', 'GDPR_SensitivePersonalData']

bound = fe.boundaries(0.5, 0.8, 0.1)

mod = fe.real_learning_module(len(skills), 4, 'Utilities/Resultat/Artikel/IDn.json', 'Utilities/Resultat/Artikel/Individer', manipulation_path = 'Utilities/Resultat/Artikel/Manipulationer.json', boundaries = bound)
trial_study = fe.study('Artikel', mod)
trial_study.describe()
trial_study.do_tests()
trial_study.summarise_results()
