import warnings
warnings.simplefilter(action='ignore')#, category=FutureWarning

import prepro_d
import engine

import sys
import os

# DATA_PATH = './data'
# PLOT_PATH = './plots'

# DF_NAME = 'wfpvam_foodprices.csv'

if __name__ == '__main__':
    
    #               Inputs handling for modularity
    #    
    # Option 1 :
    #   run python main.py and it will prompt for inputs
    inputs = sys.argv
    if len(inputs)<3:
        print()
        input_country   = input("Input country e.g Afghanistan : ")
        input_commodity = input("Input commodity e.g Wheat - Retail : ")
    elif len(inputs) == 3:
    #
    # Option 2 :
    #          run python main.py "Afghanistan" "Wheat - Retail"
    #or in general python main.py COUNTRY COMMODITY
        input_country = inputs[1]
        input_commodity = inputs[2]
    else:
    # 
    # Option 3 :
    #       Define inputs Manually
    #   and run with python main.py a a a
    #
        input_country = 'Afghanistan'
        input_commodity = 'Wheat - Retail'

    print('Setting Country : ',input_country)
    print('Setting commodity : ', input_commodity)


    # Standard pass for creating all the data needed for the analysis
    # use app.py Dash app if needed for sepparate calls
    # 
    main_path = os.path.dirname(os.getcwd())
    ENG = engine.engine(main_path)
    ENG.set_country_commodity(input_country,input_commodity)

    # Raw data / No normalization
    #-------------------Exploration
    #1
    ENG.plot_geo(dif=1)
    ENG.plot_geo(dif=12)
    #2 
    ENG.plot_country_prices()
    #3
    ENG.plot_country_region_prices()
    ENG.plot_world_region_country_prices()
    #-------------------Analysis
    #1
    ENG.plot_decompose()
    #2
    ENG.plot_get_scope()



    #Normalization, MinMax
    #2 + 3 Normalized
    SCALER = prepro_d.normalizer(ENG.df_full,input_commodity)
    SCALER.hash_all_countries()
    ENG.df_full = SCALER.df_full_normalized
    ENG.set_country_commodity(input_country,input_commodity)
    ENG.name += '_normalizedMaxMin'
    #2 norm
    ENG.plot_country_prices()
    #3 norm
    ENG.plot_country_region_prices()
    ENG.plot_world_region_country_prices()

    #-------------------Analysis
    #1
    ENG.plot_decompose()
    #2
    ENG.plot_get_scope()