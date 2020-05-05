import pandas as pd
from itertools import chain
from ast import literal_eval
from sklearn.metrics.pairwise import cosine_similarity
from geopy import distance


# dataframe of all vectorized practitioners
vectorized = pd.read_csv('recdf.csv', index_col=[0])
# Remove unnecessary column - number of insurances accepted
vectorized.drop(['num_ins'], axis=1, inplace=True)

# dataframe of cleaned practitioner info for frontend
response = pd.read_csv('response_df.csv', index_col=[0])
# for the responses for patients, fill any missing values with "N/A"
response.fillna(value='N/A', inplace=True)

# dataframe of latitude and longitude coordinates for each zip code 
zipsdf = pd.read_csv('zip_lat_long.csv')

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
all_plans = {p: find_plans(p) for p in providers}

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




class Recommendation:

    def __init__(self, vectorized, response, zipsdf, gender, new_patient, need_ins, langs, specs, ins_s, _id, zipcode, rec_input, n):
        self.vectorized = vectorized
        self.response = response
        self.zipsdf = zipsdf
        self.gender = gender
        self.new_patient = new_patient
        self.need_ins = need_ins
        self.langs = langs
        self.specs = specs
        self.ins_s = ins_s
        self._id = _id
        self.zipcode = zipcode
        self.n = n

    def rec_input(self, gender, new_patient, need_ins, langs, specs, ins_s):
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
        series_template = {x:0 for x in testdict}
        
        if gender == 1:
            series_template['Gender'] = 1
        elif gender == 0:
            series_template['Gender'] = 0
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
            if ins == 'na':
                pass
            else:
                series_template['{}'.format(ins)] = 1
            
        for lang in langs: 
            series_template['{}'.format(lang)] = 1
            
        return pd.DataFrame(series_template, index=[0])
    
    def description(self, _id):
        name = list(response.loc[response['_id'] == _id]['Name'])[0] + ", " + list(response.loc[response['_id'] == _id]['Title'])[0]
        address = list(response.loc[response['_id'] == _id]['Address'])[0]
        gender = list(response.loc[response['_id'] == _id]['Gender'])[0].title()
        languages = (", ").join(sorted(literal_eval(list(response.loc[response['_id'] == _id]['Languages'])[0])))
        specs = (", ").join(sorted(literal_eval(list(response.loc[response['_id'] == _id]['Specialties'])[0])))
        bio = list(response.loc[response['_id'] == _id]['Bio'])[0]
        insurances = (", ").join(sorted(literal_eval(list(response.loc[response['_id'] == _id]['Insurances'])[0])))
        
        desc = []
        desc.append("Name: " + name)
        desc.append("Address: " + address)
        desc.append("Gender: " + gender)
        desc.append("Language(s): " + languages)
        desc.append("Specialty/ies: " + specs)
        desc.append("Bio: " + bio)
        desc.append("Insurances Accepted: " + insurances)
               
        return desc
    
    def find_latlong(self, zipcode):
        zipcode = int(zipcode)
        lat = list(zipsdf.loc[zipsdf['ZIP'] == zipcode]['LAT'])[0]
        long = list(zipsdf.loc[zipsdf['ZIP'] == zipcode]['LNG'])[0]
        loc = (lat, long)

        return loc

    
    def find_distance(self, _id, zipcode):
        zip_interest = Recommendation.find_latlong(self, zipcode)
        lat = vectorized[vectorized['_id'] == _id]['Lat'].values[0]
        long = vectorized[vectorized['_id'] == _id]['Long'].values[0]
        from_dist = (lat, long)
        
        return round(distance.distance(zip_interest, from_dist).miles, 2)
    
    def cos_sim(self, vectorized, recinput, n, zipcode):
        cosine_similarities = cosine_similarity(vectorized.iloc[:, 3:], recinput) 
        recdf = pd.DataFrame({'_id': vectorized['_id'], 'sim': list(cosine_similarities)})
        recdf['sim'] = recdf['sim'].apply(lambda x: x[0])
        rec_df = recdf.sort_values(by = 'sim', ascending=False).reset_index().loc[0:n-1]
        rec_df.drop(['index'], axis = 1, inplace = True)
        rec_df['distance'] = rec_df['_id'].apply(lambda x: Recommendation.find_distance(self, x, zipcode))
        rec_df = rec_df.sort_values(by='distance', ascending = True).reset_index()
        rec_df.drop(['index'], axis = 1, inplace = True)
        recommendations = []
        for i in rec_df['_id']:
            recommendations.append(Recommendation.description(self, i))

        return recommendations