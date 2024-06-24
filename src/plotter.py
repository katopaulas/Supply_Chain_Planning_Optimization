import plotly.express as px
import plotly.graph_objects as go
import plotly
from plotly.subplots import make_subplots
import numpy as np

import os
import pandas as pd

# PLOT_PATH = './plots'

def is_numeric(col):
    try:
        pd.to_numeric(col)
        return True
    except:
        return False

class picasso(object):
    """
        Plotter class for orchestrating the needs for the analysis

    """
    def __init__(self, plot_path):
        self.PLOT_PATH = plot_path
    
    def geo_plot(self, df, counties = [], locs = 'name',
                    color_col = 'price_dif', name = 'test'):

        counties = counties.merge(df,
                                 left_on=['name'], 
                                 right_on=['adm1_name'])
        counties = counties[['name','price_dif','geometry']]

        fig = px.choropleth(counties, 
                            geojson=counties.__geo_interface__, 
                            locations=locs,
                            color=color_col,
                            featureidkey="properties.name",
                            title=name + " difference color map"
                              )

        fig.update_geos(fitbounds='locations',visible=False)
        name+='_geo.html'
        save_path = os.path.join(self.PLOT_PATH,name)
        fig.write_html(save_path)
        return fig

    def geo_plot_with_scope(self, df, counties = [], locs = 'adm0_name',
                    color_col = 'mp_price', name = 'test',scope = 'asia'):
        name += str(scope) + "Price color map"
        fig = px.choropleth(df, 
                            geojson=counties, 
                            locations=locs,
                            color=color_col,
                            featureidkey='properties.name',
                                   scope=scope,
                                   title=name
                              )
        
        name+= '.html'
        save_path = os.path.join(self.PLOT_PATH,name)
        fig.write_html(save_path)
        return fig

    def plot_df(self, df, name ='', save=1):
        t=df.index
        fig = go.Figure()
        
        for col in df.columns:
            if not is_numeric(df[col]):
                continue
            fig.add_trace(
                go.Scatter(x=t, y= df[col]
                , name=col)
                        )
        fig.update_layout(
            title = name + " price (average on regions)"
            )

        #save process
        if save:
            s1 = os.path.join(self.PLOT_PATH, name + '.html')
            fig.write_html(s1)

        return fig


    def plot_decomposition(self, seasonal_decomposition):
        seasonal_decomposition_fig = seasonal_decomposition.plot()
        seasonal_decomposition_fig = plotly.tools.mpl_to_plotly(seasonal_decomposition_fig)
        seasonal_decomposition_fig.update_layout(title = 'Seasonal Decomposition', title_x=0.1,
                                                 )
        return seasonal_decomposition_fig

    def plot_sarimax(self, ts,preds_df,conf=0.05,name='test'):
        conf = float(conf)

        #add traces
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ts.index, y= ts, name='historic values'
            #,mode='markers'
                    ))
        fig.add_trace(go.Scatter(x=preds_df.index, y= preds_df['mean'],
                        name = r'Predicted mean',
                    ))

        fig.add_trace(go.Scatter(x=preds_df.index, y= preds_df['mean_ci_lower'], 
                        line_color = 'rgba(0,0,0,0)',
                        showlegend = False
                    ))
        fig.add_trace(go.Scatter(x=preds_df.index, y= preds_df['mean_ci_upper'],
                        line_color = 'rgba(0,0,0,0)',
                        name = r'95% confidence interval',
                        fill='tonexty', fillcolor = 'rgba(255, 0, 0, 0.2)'
                    ))
        
        #save process
        if 1:
            s1 = os.path.join(self.PLOT_PATH, name+'_pred.html')
            fig.write_html(s1)

        return fig

    def plot_seasonal_decompose(self, result, dates, title = "Seasonal Decomposition"):
        x_values = dates if dates is not None else np.arange(len(result.observed))
        fig = (
            make_subplots(
                rows=4,
                cols=1,
                subplot_titles=["Observed", "Trend", "Seasonal", "Residuals"],
            )
            .add_trace(
                go.Scatter(x=x_values, y=result.observed, mode="lines", name='Observed'),
                row=1,
                col=1,
            )
            .add_trace(
                go.Scatter(x=x_values, y=result.trend, mode="lines", name='Trend'),
                row=2,
                col=1,
            )
            .add_trace(
                go.Scatter(x=x_values, y=result.seasonal, mode="lines", name='Seasonal'),
                row=3,
                col=1,
            )
            .add_trace(
                go.Scatter(x=x_values, y=result.resid, mode="lines", name='Residual'),
                row=4,
                col=1,
            )
            .update_layout(
                height=900, title=f'<b>{title}</b>', margin={'t':100}, title_x=0.5, showlegend=False
            )
        )
        #save process
        s1 = os.path.join(self.PLOT_PATH, title+'_seasonal_decomose' + '.html')
        fig.write_html(s1)
        return fig


