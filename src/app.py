
import dash
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import engine
import os

print(os.getcwd())
main_path = os.path.dirname(os.getcwd())
engine = engine.engine(main_path)

COUNTRY_DICT = {'AFG':'Afghanistan'}
COMMODITY_LIST = ['Wheat - Retail']
PREDICTION_MODELS = ['arima']

DATA = ''

def app_skeleton():
    
    
    app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])


    app.layout = html.Div([
        html.Div(id='hidden-div', style={'display':'none'}),
        html.Div(id='hidden-div1', style={'display':'none'}),
        html.Div(id='hidden-div2', style={'display':'none'}),
        
        dbc.Row([
            # Left column / misc + graphs
            dbc.Col([
                
                # button row/ load data
                dbc.Row([
                    html.Button('Load/Reload Data', id='submit-val', n_clicks=0),
                    #html.Button('Load,prepro Data', id='data_prepro_load', n_clicks=0),
                    ])
                ,
                # Graph row
                dbc.Row(id = 'chart_row'),
                
                #dbc.Row(id = 'map_row'),
                dbc.Row([
                    dbc.Col(dcc.Dropdown(
                        options = [{'label':i,'value':i} for i in PREDICTION_MODELS],
                        id='pred_dropdown',
                        style={'margin-right': '20px'},
                        searchable=False,
                        placeholder= 'Choose prediction model'
                                    )),
                    dbc.Col(html.Button('Train/Retrain', id='train_button', n_clicks=0),)
                    ,
                    dbc.Col(html.Div(dcc.Input(id='pred_window_input', type='text',placeholder='Select forecast window'))
                    ),
                    dbc.Col(html.Button('Plot prediction', id='pred_button', n_clicks=0),)
                    
                    
                    ]),
                 dbc.Row(id='prediction_row'),   

                html.Div()#source recommend
                ])
            ,
            
            # Right column/ dropdowns +..
            dbc.Col([
                dbc.Row([
                dbc.Col([
                    html.Div(dcc.Input(id='target_country', type='text',placeholder='Type country (eg AFG)'))
                    ,
                    dcc.Dropdown(
                        options = [{'label':i,'value':i} for i in COMMODITY_LIST],
                        id='commodity',
                        style={'margin-right': '20px'},
                        placeholder= 'Commodity type'
                        ),
        
                    dcc.Dropdown(
                    options = [{'label':i,'value':i} for i in ['WORLD','TARGET','REGION', 'TARGET_REGION','WORLD_TARGET_REGION']],
                    id='data_focus',
                    style={'margin-right': '20px'},
                    searchable=False,
                    placeholder= 'Dataset focus'
                                )
                    ]),
                
                dbc.Col([
                    dbc.Row([
                        html.Button('Plot geo map', id='geomap_button', n_clicks=0),
                        html.Button('Plot price', id='priceplot_button', n_clicks=0),
                        html.Button('Plot Decompose', id='decompose_button', n_clicks=0)
                        ]),
                   dbc.Row(
                       html.Div(dcc.Input(id='dif_geo', type='text',placeholder='Difference in months'))
                       
                       )
                    ])
                    
                    ])
                
                
                ,
                html.Div(
                    [
                      #dcc.Input(),
                      html.Br(),
                      #dcc.Input()
                    ]
                    ),
                
                dbc.Row(id='decompose_row')
                
                ,
                html.Div(
                    [
                      #dcc.Input(),
                      html.Br(),
                      #dcc.Input()
                    ]
                    ),
                dbc.Row(id = 'map_row'),
                
                
                    ])#,xs = 10, sm=10, md=10, lg=10
                
                ]),

           # dbc.Col([
               

            #    ])
        
        
        
        
            #])
        ])
    
    
    # @app.callback(
    #     Output('map_row','children'),
    #     Input()
        
    #     )
    # def map_charts():
        
        
    #     return dcc.Graph(id='map_chart',figure=fig,)
    
    @app.callback(
        Output(component_id='hidden-div', component_property='children'),
        [Input('commodity','value'),
        Input('submit-val','n_clicks')],
        State('target_country', 'value')
        )
    def set_country(com, n_clicks, input_value):
        if not com or not n_clicks or not input_value:
            raise PreventUpdate
        try:
            country = COUNTRY_DICT[input_value]
        except Exception:
            country = 'Afghanistan'
            
        engine.set_country_commodity(country,com)
        
        #print('com',com)
        return 'You\'ve entered "{}" and clicked {} times'.format(input_value, n_clicks)


    @app.callback(
        Output('chart_row','children'),
        Input('data_focus','value'),
        Input('priceplot_button','n_clicks'),
        )
    def data_charts(data_focus,n_clicks):
        if not data_focus or not n_clicks:
            raise PreventUpdate
        
        fig = engine.get_data_graph(data_focus)
        return  dcc.Graph(id='data_chart', figure=fig,)

    @app.callback(
        Output('map_row','children'),
        Input('geomap_button','n_clicks'),
        State('dif_geo','value')
        )
    def geo_charts(n_clicks,dif):        
        if not n_clicks:
            raise PreventUpdate
        if not dif:
            dif=1
        else:
            dif = int(dif)
        fig = engine.plot_geo(dif)
        return  dcc.Graph(id='g_chart', figure=fig,)
    
    
    
    @app.callback(
        Output('decompose_row','children'),
        Input('decompose_button','n_clicks')
        )
    def decompose_charts(n_clicks):
        
        if not n_clicks:
            raise PreventUpdate

        fig = engine.plot_decompose()
        return  dcc.Graph(id='decompose_chart', figure=fig,)
    
    
    @app.callback(
        Output('hidden-div1','children'),
        Input('pred_dropdown','value'),
        Input('train_button','n_clicks')
        )
    def train_retrain(model_pick,n_clicks):
        
        if not model_pick or not n_clicks:
            raise PreventUpdate
            
        engine.train_model()
        return 'Done'
    
    @app.callback(
        Output('hidden-div2','children'),
        Input('pred_dropdown','value')
        )
    def pick_model(model_pick):
        
        if not model_pick:
            raise PreventUpdate
            
        engine.set_model(model_pick)
        return 'Done'
    
    @app.callback(
        Output('prediction_row','children'),
        Input('pred_button','n_clicks'),
        State('pred_window_input','value')
        )
    def predict_chart(n_clicks, window):
        
        if not n_clicks or not window:
            raise PreventUpdate
        
        engine.predict(window)
        fig = engine.plot_arima()
        return dcc.Graph(id='pred_chart', figure=fig,)
    
    
    
    
    return app
    
    
# Running the Dash app.
if __name__ == '__main__':
    app = app_skeleton()
    app.run_server(
        port=8050,
        host='0.0.0.0',
        debug=True)