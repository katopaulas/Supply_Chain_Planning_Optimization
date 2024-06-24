
DATA_FOCUS = ['WORLD','TARGET','REGION', 'TARGET_REGION','WORLD_TARGET_REGION']
DATA_PATH = '/data'
#PLOT_PATH = '/plots'
DF_NAME = 'wfpvam_foodprices.csv'

COUNTRY_COLUMN   = 'adm0_name'
COMMODITY_COLUMN = 'cm_name'
NUMERIC_COLUMN   = 'mp_price'


import pandas as pd
import os

import prepro_d
import plotter
import ml
import geo_helper

class engine():
    '''
        Engine object that handles all computations.
        Inputs : str, mainpath of the project
        
        Important Function before running:
            set_country_commodity(country,commodity) : sets up data and basic pandas dataframes
            After this function every function in the engine can be used independently
            
    '''
    def __init__(self,mainpath):
        super().__init__()
        self.mainpath = mainpath
        self.DATA_PATH = os.path.join(mainpath,'data')
        self.PLOT_PATH = os.path.join(mainpath,'plots')
        self.plotter = plotter.picasso(self.PLOT_PATH)
        self.GEO = geo_helper.geo(self.DATA_PATH)

        self.country,self.commodity ='',''
        self.name = ''
        datapath = os.path.join(self.DATA_PATH, DF_NAME)
        self.df_full = pd.read_csv(datapath).fillna(method='bfill')
        
        self.plot_dictionary = {'WORLD':self.plot_world_prices,
                         'TARGET':self.plot_country_prices,
                         'REGION':self.plot_region_prices, 
                         'TARGET_REGION':self.plot_country_region_prices,
                         'WORLD_TARGET_REGION':self.plot_world_region_country_prices
                         }
        self.mode= ''; self.predictions = [];
        
        
    def set_country_commodity(self,country,commodity):
        self.country = country
        self.commodity = commodity
        self.name = self.country + '_' + self.commodity 
        
        #set data
        self.df_country  = self.target_country_commodity(self.df_full,country,commodity)

        self.df_avg      = self.country_data()
        self.df_world    = self.world_data()
        self.df_region   = self.region_data()
        print('SET DATA STATUS --OK--')
            
    def target_country_commodity(self, df, country, commodity):
        df_country = df[df[COUNTRY_COLUMN] == country]

        #self.cur_name = df_country['cur_name'].values[0]
        df_country_commodity = df_country[df_country[COMMODITY_COLUMN] == commodity]
        df_country_commodity = prepro_d.cleanse(df_country_commodity)
        return df_country_commodity    
        
    def get_data_graph(self, data_focus):
        if not len(self.country):
            print('NEED TO LOAD A COUNTRY FIRST')
            
        if data_focus not in DATA_FOCUS:
            print('NOT CORRECT FOCUS')
        
        f = self.plot_dictionary[data_focus]
        return f()
     
    def plot_geo(self,dif=1):
        regions = prepro_d.get_regions(self.DATA_PATH,self.country)
        df_recent, dict_regions = prepro_d.hash_regions(self.df_country,dif)
        
        if len(df_recent) == 1:
            df_recent['name'] = self.country
            countries_json,_ = self.GEO.asia_countries_json()
            df_recent = df_recent[['name','price_dif']]
            #print(df_recent.dropna(axis=1))
            return self.plotter.geo_plot_with_scope(df_recent,
                counties=countries_json,
                locs='name',
                color_col='price_dif',
                name = self.name + '_dif= '+ str(dif))

        return self.plotter.geo_plot(df_recent,counties=regions,name = self.name + '_dif= '+ str(dif))
    
    def plot_get_scope(self):
        countries_json,_ = self.GEO.asia_countries_json()
        
        df_recent = prepro_d.get_recent_vals(self.df_full, self.commodity,self.DATA_PATH)
        return self.plotter.geo_plot_with_scope(df_recent,counties=countries_json,name =self.name+ '_scoped=')
    
    
    def plot_world_prices(self):
        return self.plotter.plot_df(self.df_world, name =self.name+ 'Global scale, Simple Average')
    
    def plot_region_prices(self):
        return self.plotter.plot_df(self.df_region, name =self.name+ 'Asia scale, Simple Average')
    
    def plot_country_prices(self):
        return self.plotter.plot_df(self.df_avg, name = 'Target Country=' + self.name + 'Simple Average')
    
    def plot_world_region_country_prices(self):
        df_compare = self.df_avg.copy()
        df_compare['mp_price_region'] = self.df_region['mp_price']
        df_compare['mp_price_world']  = self.df_world['mp_price']
        return self.plotter.plot_df(df_compare,name = self.name + '_Comparing AFG vs WORLD vs REGION')
        
    def plot_country_region_prices(self):
        df_compare = self.df_avg.copy()
        df_compare['mp_price_region'] = self.df_region['mp_price']
        return self.plotter.plot_df(df_compare, name =self.name +  '_Comparing AFG vs REGION')
    
    def world_data(self):
        df_world  = prepro_d.clean_and_sort(self.df_full)
        df_world = df_world.groupby('DATE').max()
        return df_world
    
    def region_data(self):
        df_region = prepro_d.target_region(self.df_full,self.commodity,self.DATA_PATH)
        df_region = prepro_d.clean_and_sort(df_region)
        return df_region.groupby('DATE').max()#.mean()
    
    def country_data(self):
        df_country = prepro_d.clean_and_sort(self.df_country)
        return df_country.groupby('DATE').max()#.mean()
    
    def plot_decompose(self):
        ts = self.df_avg[NUMERIC_COLUMN]
        seasonal_decomposition = ml.decompose_ts(ts, model = 'additive')
        return self.plotter.plot_seasonal_decompose(seasonal_decomposition,ts.index,title=self.name)
    
    def set_model(self, mode='arima'):
        self.mode = mode
        self.ts = self.df_avg[NUMERIC_COLUMN]
        self.ts = self.ts.asfreq('M',method='bfill')
        
    def train_model(self):
        self.model = ml.train_model(self.ts,mode = self.mode)
        #self.model = ml.auto_arima_ts(self.ts)
   
    def predict(self,window=1):

        self.predictions = ml.predict(self.model,window=window,mode=self.mode)
        
    def plot_arima(self):
        return self.plotter.plot_sarimax(self.ts, self.predictions,name=self.name)
    
    
