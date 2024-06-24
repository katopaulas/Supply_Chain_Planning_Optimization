import json
import geopandas as gpd
import os        


class geo(object):
    """
        Skeleton for geo class in order to be able to expand
        to modularity in geo plots.
        
        Visit https://code.highcharts.com/mapdata/ (1)
        to download geojson for country needed, place in data path
        The format at the moment is (first 2 letters of country)-all.geo.json
                                                eg af-all.geo.json
        
        TODO: When expanded a dictionary {country_name : country_id_file}
        will be needed to be implemented as in prepro_d.py
    """
    def __init__(self, datapath):
        super(geo, self).__init__()
        self.DATAPATH = datapath
        
    def download_counties(self,country):
        # predownloaded afghanistan and Tajikistan
        # Uncomment below if you want to download AFG again
        # Else visit (1) and download the geojson.
        
        print('DOWNLOAD GEOJSON FROM')
        print('https://code.highcharts.com/mapdata/')
        print('PLACE IT TO DATA FOLDER')
        return
        # Custom for afghanistan
        # with urlopen('https://gist.githubusercontent.com/notacouch/f97501dbcfb44e14cabd6d5ed710e10b/raw/511421c31f6a0ad870bc47dbc0d9826c5d315363/afghanist-provinces-districts--cities-demo.json') as response:
        #     counties = json.load(response)
        #     p = os.path.join(self.DATAPATH,'counties_AFG.json')
        #     with open(p, 'w') as f:
        #         json.dump(counties, f, ensure_ascii=False)

    def get_counties(self,country):
        # Retrieve regions in country
        p = os.path.join(self.DATAPATH,str(country)[:-1] + '-all.geo.json')
        counties= gpd.read_file(p)

        return counties.to_crs(epsg=4326)
        # p = os.path.join(self.DATAPATH,'counties_AFG.json')
        # with open(p, 'r') as f:
        #     counties = json.load(f)
        #     for feature in counties['features']:
        #         feature['id'] =  feature['properties']['name']
        #     return counties.to_crs(epsg=4326)

    def asia_countries_json(self):
        # return json for geo and list of names
        world_data = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        asia  = world_data[world_data.continent=='Asia']
        
        countries = asia['name']
        countries.loc[-1] = 'Iran  (Islamic Republic of)'
        asia_json = json.loads(asia.to_json())
        return asia_json,countries
