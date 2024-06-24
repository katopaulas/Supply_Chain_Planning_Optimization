import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
#from sklearn.ensemble import RandomForestRegressor

# Basic Machine learning library for
# Seasonal decomposition
# Autoregressive model training


MODELS_DICT = {#'RF':RandomForestRegressor,
               'arima': sm.tsa.statespace.SARIMAX}

def decompose_ts(ts,model = 'additive'):
    ts = ts.asfreq('M',method='bfill')
    result = seasonal_decompose(ts, model=model)
    return result

def train_model(ts,mode='arima'):
    #f = MODELS_DICT[mode]
    model = sm.tsa.statespace.SARIMAX(ts, trend='c', 
                                      order=(2,1,0),
                                      seasonal_order=(2,1,0,12))
    results = model.fit(disp=False)
    print('Train completed')
    return results
    
def predict(result_model, window =1, conf = 0.05,mode='arima'):
    window = int(window)
    pred = result_model.get_forecast(window).summary_frame(alpha=conf)
    return pred
    
def auto_arima_ts(data):
    #pip install pmdarima
    import pmdarima
    #from pyramid.arima import auto_arima
    stepwise_model = pmdarima.auto_arima(data, start_p=1, start_q=1,
                               max_p=3, max_q=3, m=12,
                               start_P=0, seasonal=True,
                               d=1, D=1, trace=True,
                               error_action='ignore',  
                               suppress_warnings=True, 
                               stepwise=True)
    
    print(stepwise_model.aic())
    
    return stepwise_model
    