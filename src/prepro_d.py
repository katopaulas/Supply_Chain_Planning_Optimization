import pandas as pd
import os
import geo_helper

############## BASIC PREPROCESSING FUNCTIONS ###############
##############     AND A NORMALIZER CLASS    ###############

NUMERIC_COLUMN   = 'mp_price'
COUNTRY_COLUMN   = 'adm0_name'
REGION_COLUMN    = 'adm1_name'
COMMODITY_COLUMN = 'cm_name'
COMMODITY_VALUE_COLUMN = 'mp_price'

DICT_countries = {'Afghanistan': 'afg',
                  'Tajikistan': 'tjk'}

def cleanse(df):
    to_drop = ['adm0_id', 'adm0_name', 'adm1_id','mkt_id', 'cm_id', 'cm_name',
               'cur_id', 'cur_name', 'um_name','um_id', 'mkt_name','mp_commoditysource',
               'pt_id', 'pt_name']
    return df.drop(to_drop,axis=1, errors='ignore')

def sort_by_date(df):
    #df = pd.read_csv(name)
    df.columns = ['MONTH' if x=='mp_month' else x for x in df.columns]
    df.columns = ['YEAR' if x=='mp_year' else x for x in df.columns]
    df['DATE'] = pd.to_datetime(df[['YEAR', 'MONTH']].assign(DAY=1))
    df.drop(['YEAR', 'MONTH'],axis =1,inplace=True)
    df = df.sort_values('DATE')
    df.index = df['DATE']
    
    return df.drop('DATE',axis=1, errors='ignore')
 
def clean_and_sort(df):
    df_out = cleanse(df)
    df_out = sort_by_date(df_out)
    return df_out

def target_region(df,commodity,datapath):
    geo = geo_helper.geo(datapath)
    _,countries_list = geo.asia_countries_json()
    
    df_region = df[df[COUNTRY_COLUMN].isin(countries_list)]
    df_region_com = df_region[df_region[COMMODITY_COLUMN] == commodity]
    return df_region_com
    
def get_regions(datapath,country='AFG'):
    country = DICT_countries[country]

    geo = geo_helper.geo(datapath)
    #FILE PREPROCESS
    p = os.path.join(datapath,str(country)[:-1]+'-all.geo.json')
    if not os.path.isfile(p):
        geo.download_counties(country)
        print('Downloaded json file for counties/regions')
        
    return geo.get_counties(country)

def hash_regions(df,dif=1):
    
    unique_regions = df[REGION_COLUMN].unique()

    dict_dfs_per_regions = {key:0 for key in unique_regions} 
    df_recent = pd.DataFrame(columns = df.columns)

    if not unique_regions[0] == unique_regions[0]:
        difference = df[COMMODITY_VALUE_COLUMN].values[-1] \
                    - df[COMMODITY_VALUE_COLUMN].values[-1-dif]
        df_temp = df.iloc[-1,:].copy()
        df_temp[COMMODITY_VALUE_COLUMN] = difference
        new_df = pd.DataFrame([df_temp])
        df_recent = pd.concat([df_recent, new_df], ignore_index=True)
        #df_recent = df_recent.append(df_temp, ignore_index=True)
    else:
        for i,name in enumerate(unique_regions):
            region_df = df[df[REGION_COLUMN] == name]
            dict_dfs_per_regions[name] = region_df

            if len(region_df):
                difference = region_df[COMMODITY_VALUE_COLUMN].values[-1] \
                    - region_df[COMMODITY_VALUE_COLUMN].values[-1-dif]
                
                region_df.loc[region_df.index[-1],COMMODITY_VALUE_COLUMN] = difference
                new_df = pd.DataFrame([region_df.iloc[-1,:]])
                df_recent = pd.concat([df_recent, new_df], ignore_index=True)
                #df_recent = df_recent.append(region_df.iloc[-1,:], ignore_index=True)

    df_recent.columns = ['price_dif' if x=='mp_price' else x for x in df_recent.columns]    
    
    return df_recent, dict_dfs_per_regions

def get_recent_vals(df,commodity,datapath):
    #df = df_region
    df_region = target_region(df, commodity,datapath)
    df_region = df_region[['adm0_name','mp_price']]

    countries = df_region['adm0_name'].unique()
    df_recent = pd.DataFrame()
    for country in countries:
        country_df = df_region[df_region['adm0_name'] == country]
        if len(country_df):
            #df_recent = df_recent.append(country_df.iloc[-1,:])
            new_df = pd.DataFrame([country_df.iloc[-1,:]])
            df_recent = pd.concat([df_recent, new_df], ignore_index=True)
                


        
    return df_recent




from collections import defaultdict

class normalizer():
    """
        Basic normalizer class,
        INPUTS : pandas DataFrame, with all data
        COMMODITY : str, to crop into the desired numeric col
        
        Saves scalers in dictionary DICT_scalers_per_country

    """
    def __init__(self, full_df, commodity):


        #               DATA PREPROCESS
        # Extract raw file - contains full dataset
        self.df_full = full_df[full_df[COMMODITY_COLUMN] == commodity]
        self.DICT_scalers_per_country = defaultdict(list)
        self.DICT_df_country = defaultdict()

    def hash_all_countries(self):
        df_full_normalized = pd.DataFrame()

        countries = self.df_full[COUNTRY_COLUMN].unique()

        for country in countries:
            df_country = self.hash_country(country)

            if not len(df_country):
                continue

            self.DICT_df_country[country] = df_country
            #Normalize
            # z-norm
            #df_country['mp_price'],m,s = self.normalize_z_ts(df_country['mp_price'])
            #self.DICT_scalers_per_country[country] = [m,s]
            # MaxMin norm
            df_country['mp_price'],scaler = self.normalize_01_ts(df_country['mp_price'])
            self.DICT_scalers_per_country[country] = [scaler]
            
            #df_full_normalized = df_full_normalized.append(df_country)
            df_full_normalized = pd.concat([df_full_normalized, df_country], ignore_index=True)
        self.df_full_normalized = df_full_normalized

    def hash_country(self,country_name):
        df_country = self.df_full[self.df_full[COUNTRY_COLUMN] == country_name]
        return df_country

    def normalize_z_ts(self,ts):
        #ts : pandas series object
        m,s = ts.mean(), ts.std()
        return (ts-m)/s,m,s

    def normalize_01_ts(self,df):
        from sklearn import preprocessing
        min_max_scaler = preprocessing.MinMaxScaler()
        df_normed = min_max_scaler.fit_transform(df.values.reshape(-1,1))
        return df_normed,min_max_scaler

    def normalize_z(self,df):
        m,s = df[NUMERIC_COLUMN].mean(), df[NUMERIC_COLUMN].std()
        df[NUMERIC_COLUMN] = (df[NUMERIC_COLUMN] - m)/s

        return df, m ,s