import pandas as pd
from itertools import chain
from ast import literal_eval
from sklearn.metrics.pairwise import cosine_similarity

# dataframe of all vectorized practitioners
vectorized = pd.read_csv('recdf.csv', index_col=[0])
# Remove unnecessary column - number of insurances accepted
vectorized.drop(['num_ins'], axis=1, inplace=True)

# dataframe of cleaned practitioner info for frontend
response = pd.read_csv('response_df.csv', index_col=[0])
# for the responses for patients, fill any missing values with "N/A"
response.fillna(value='N/A', inplace=True)

# make a list of all insurance plans 
insurances = list(vectorized.iloc[:, 40:164].columns)

def find_providers():
    """
    The insurances that are found in the data are formatted as "provide-plan". 
    This function returns solely the providers, which will make it easier for patients to select insurance plans on the front end.
    
    Returns: 
    list[str]
    """
    # append to an empty list to just find providers 
    providers = []
    for i in insurances:
        # split at the "-" in each string and retrieves only the provider information 
        providers.append(i.split('-')[0].title())
    #sorted alphabetically 
    providers = sorted(list(set(providers)))
    return providers

providers = find_providers()

def find_plans(p):
    """
    The insurances that are found in the data are formatted as "provide-plan". 
    This function returns solely the plans that correspond with a provider, which will make it easier for patients to select insurance plans on the front end.
    
    Parameters: 
    p (str): Provider name

    Returns: 
    list[str]
    """
    # append to an empty list to find a list of plans for each provider
    plans = []
    for i in insurances:
        # checks to see whether the insurance corresponds with the given provider, p
        if p.lower() == i.split('-')[0]:
            plans.append(i)
    return plans

# makes a dictionary with a list of all plans underneath each provider
all_plans = {k: find_plans(p) for p in providers}

# makes a list of all languages spoken by all practitioners
languages = list(vectorized.iloc[:, 164:].columns)

# makes a list of all specialties offered by all providers
specialties = list(vectorized.iloc[:, 7:40].columns)

def rec_input(gender, new_patient, need_ins, langs, specs, ins_s):
    """
    Vetorizes patient input so that it can be passed into the cosine similarity algorithm.
    
    Parameters: 
    gender (bool): gender
    new_patient (bool): whether the patient is looking for a new practitioner
    need_ins (bool): whether the patient needs the practitioner to accept insurance
    langs (str): language spoken
    specs (str): specialty needed
    ins_s (str): insurance plan

    Returns:
    df (vector) of patient input

    """
    tests = vectorized.iloc[:, 3:].loc[0]
    testdict = tests.to_dict()
    # allows us to create an empty template dataframe for our patient input
    series_template = {x:0 for x in testdict}
    
    if gender == 1:
        series_template['Gender'] = 1
    elif gender == 0:
        series_template['Gender'] = 0
    # if there's no gender preference, make this value 0.5 so as not to sway results in any direction
    elif gender == 2:
        series_template['Gender'] = 0.5
        
    if new_patient == 1:
        series_template['New_Patients'] = 1
        
    series_template['num_lang'] = len(langs)
    if need_ins == 1:
        series_template['insurance'] = 1
        
    for spec in specs: 
        series_template['{}'.format(spec)] = 1
        
    for ins in ins_s:
        series_template['{}'.format(ins)] = 1
        
    for lang in langs: 
        series_template['{}'.format(lang)] = 1
        
    return pd.DataFrame(series_template, index=[0])