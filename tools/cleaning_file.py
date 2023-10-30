import pandas as pd
from geopy.geocoders import Nominatim
import time
from tqdm import tqdm
import pycountry



def get_country(city):
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.geocode(city)
    except:
        return None
    if location is not None:
        return location.raw['display_name'].split(",")[-1].strip()
    else:
        return None

def add_countries_continent(file):
    known_places=pd.read_csv('data\lix_scrapper\location_data.csv').set_index('city',drop=False)
    known_countries=pd.read_csv('data\lix_scrapper\continent_data.csv').set_index('country',drop=False)
    df=pd.read_excel(file)
    try:
        df.drop(columns=['country', 'continent'],inplace=True)
    except:
        None
    cities=df['linkedin_location'].to_list()
    countries=[]
    continents=[]
    for i,city in tqdm(enumerate(cities)):
        if not isinstance(city,str):
            city=''
        if 'Singapore' in city:
            country='Singapore'
            continent='Asia'
        elif city in known_places.index.to_list():
            continent=known_places.loc[city]['continent']
            country=known_places.loc[city]['country']
        else :
            country=str(get_country(city))
            if country in known_countries.index.to_list():
                continent=known_countries.loc[country]['continent']
            else: 
                continent='Unknown'
            try:
                s=pd.DataFrame({'city':city,'country':country,'continent':continent},index=[city])
                known_places=pd.concat([known_places,s])
            except:
                None
        countries.append(country)
        continents.append(continent)
    known_places.to_csv('data\lix_scrapper\location_data.csv',index=False)
    df['country']=countries
    df['continent']=continents
    df.to_excel(file,index=False)
    print('added countries and continent')

def clean_country_continent(file):
    df=pd.read_excel(file)
    df['country']=df['country'].str.replace('.*Singapore.*','Singapore', regex=True)
    df['country']=df['country'].str.replace('.*Italia.*','Italia', regex=True)
    df['continent']=df['continent'].replace(['.*Asia.*','.*Europe.*'],['Asia','Europe'], regex=True)
    df.to_excel(file,index=False)


def clean_company_size(file:str):
    df=pd.read_excel(file)
    sizes=[]
    for size in df['Company size']:
        try:
            sizes.append(size.split('employees')[0]+ 'employees')
        except:
            sizes.append('Unknown')
    df["Company size"]=sizes
    df.to_excel(file, index=False)
    print('Size cleaned')

# clean_company_size('data\quantumapalooza\extended_data.xlsx')

def delete_french_data():
    index=[]
    df=pd.read_csv('data\lix_scrapper\companies_data.csv')
    print(df.columns)
    size=df.shape[0]
    for i in range(size):
        french_size=df.loc[i]["Taille de l’entreprise"]
        try : 
            if len(french_size)>=1 : 
                index.append(i)
        except :
            a=1
    print(len(index))
    df.drop(index, inplace=True)
    df.to_csv('data\lix_scrapper\companies_data.csv')
 
def remove_blacklisted_companies(file):
    Black_list=['quantum management services ltd.','Maxim Recruitment Limited','keysight technologies',\
                'quantum health','quantum world technologies inc.']
    Grey_list=['thales']
    df=pd.read_excel(file)
    companies=df['Organisation Name']
    drop_indexes=[]
    for index in companies.index.to_list():
        for bl_companie in Black_list:
            if companies.loc[index] == bl_companie:
                drop_indexes.append(index)
    df.drop(drop_indexes, inplace=True)
    df.to_excel(file,index=False)
    print('Removed {} black listed companies from file'.format(len(drop_indexes)))

# remove_blacklisted_companies('data\lix_scrapper\offers.xlsx')


cluster_linkedin_category= {
    'Hardware': ['Computer Hardware Manufacturing', 'Fabrication de matériel informatique', 'Semiconductor Manufacturing'],
    'IT Services': ['IT Services and IT Consulting', 'Information Technology & Services', 'Computer and Network Security', 'Computer Networking'],
    'Research': ['Biotechnology Research', 'Research', 'Research Services', 'Think Tanks', 'Market Research'],
    'Education': ['Education Management', 'Higher Education', 'Education Administration Programs', 'E-Learning Providers'],
    'Restauration': ['Restaurants'],
    'Health': ['Medical Practices', 'Medical Equipment Manufacturing', 'Pharmaceutical Manufacturing'],
    'Construction': ['Construction', 'Bâtiment', 'Real Estate'],
    'Manufacturing': ['Computers and Electronics Manufacturing', 'Fabrication de machines automatiques', 'Chemical Manufacturing',\
                       'Appliances. Electrical. and Electronics Manufacturing', 'Industrial Machinery Manufacturing', 'Motor Vehicle Manufacturing',\
                          'Machinery Manufacturing'],
    'Human Resources': ['Staffing and Recruiting', 'Human Resources Services', 'Executive Search Services'],
    'Services': ['Business Consulting and Services', 'Services et conseil aux entreprises'],
    'Defense and Space': ['Defense and Space Manufacturing'],
    'Transportation. Logistics': ['Transportation. Logistics. Supply Chain and Storage'],
    'Telecommunications': ['Telecommunications'],
    'Financial Services': ['Financial Services','Venture Capital and Private Equity Principals'],
    'Marketing': ['Marketing Services', 'Advertising Services']
    }

def create_industry_cluster(file):
    df=pd.read_excel(file)
    domains=df['linkedin_industry_domain']
    industry_cluster=[]
    for i,domain in enumerate(tqdm(domains)):
        c=0
        for category, keywords in cluster_linkedin_category.items():
            if domain in keywords and c==0:
                industry_cluster.append(category)
                c=1
        if c==0:
            industry_cluster.append('others')
    df['Industry Cluster']= industry_cluster
    df.to_excel(file,index=False)
    print('Added cluster for linkedin domain')

# create_industry_cluster(r'data\lix_scrapper\new_offers.xlsx')
# create_industry_cluster('data\quantumapalooza\job_data_companies.xlsx')
        

def del_useless_columns(file):
    df=pd.read_csv(file)
    print(df.columns)
    df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0'],inplace=True)
    df.to_csv(file,index=False)


# del_useless_columns('data\lix_scrapper\companies_data.csv')
# del_useless_columns('data\lix_scrapper\location_data.csv')

# df=pd.read_csv('data\lix_scrapper\location_data.csv').filter(items=['country','city'])
# df2=df.drop_duplicates(subset=['country']).filter(items=['country','continent'])
# df2.to_csv('data\lix_scrapper\continent_data.csv',index=False)

# remove_blacklisted_companies(r'C:\Users\Simonis\Documents\quantum-jobs\data\lix_scrapper\offers_with_descriptions.xlsx')
# df=pd.read_excel(r'C:\Users\Simonis\Documents\quantum-jobs\data\lix_scrapper\offers_with_descriptions.xlsx')

# df = df.dropna(subset=['Description'])
# df.drop(columns=['Industry Cluster'],inplace=True)
# df.to_excel(r'C:\Users\Simonis\Documents\quantum-jobs\data\lix_scrapper\offers_with_descriptions.xlsx',index=False)
# create_industry_cluster(r'C:\Users\Simonis\Documents\quantum-jobs\data\lix_scrapper\offers_with_descriptions.xlsx')

