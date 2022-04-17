#REQUIREMENTS
from dash import dcc,html,Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
import pathlib
from app import app


#GET RELATIVE DATA FOLDER
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#LOAD DATAFRAMES
df= pd.read_excel(DATA_PATH.joinpath("DataSetLimpio.xlsx"))
df_locations=pd.read_excel(DATA_PATH.joinpath("df_locations.xlsx"))

#OBJECTS
#slider with years
slider = dcc.RangeSlider(
        id='my-range-slider', # any name you'd like to give it
        marks={
                2015: '2015',      
                2020: {'label': '2020', 'style': {'color':'#f50', 'font-weight':'bold'}},
            },
        step=1,                # number of steps between values
        min=2015,
        max=2020,
        value=[2015,2020],     # default value initially chosen
        dots=True,             # True, False - insert dots, only when step>1
        allowCross=False,      # True,False - Manage handle crossover
        disabled=False,        # True,False - disable handle
        pushable=0,            # any number, or True with multiple handles
        updatemode='mouseup',  # 'mouseup', 'drag' - update value method
        included=True,         # True, False - highlight handle
        vertical=False,        # True, False - vertical, horizontal slider
        verticalHeight=900,    # hight of slider (pixels) when vertical=True
        className='slider',
        tooltip={'always_visible':False,  'placement':'bottom'}
        )

#drop menu with the vaiable
dropList_Yvariable = dcc.Dropdown(id='y-variable', options=[{'label':'DNI Irradiance','value':'DNI'},  {'label':'Wind Speed','value':'Wind_Speed'},  {'label':'Temperature','value':'Temperature'}  ], value='DNI',clearable=False,className='button')


#slider with number of months to forecast
slider2=dcc.Slider(
        id='my-slider', # any name you'd like to give it
        marks={
                12: '1 year',
                36: '3 years',      
                60: {'label': '5 years', 'style': {'color':'#f50', 'font-weight':'bold'}},
            },
        min=0,
        max=60,
        step=3,
        value=12,      # default value initially chosen
        dots=True,             # True, False - insert dots, only when step>1
        disabled=False,        # True,False - disable handle
        updatemode='mouseup',  # 'mouseup', 'drag' - update value method
        included=True,         # True, False - highlight handle
        vertical=False,        # True, False - vertical, horizontal slider
        verticalHeight=900,    # hight of slider (pixels) when vertical=True
        className='',
        tooltip={'always_visible':False,  'placement':'bottom'}
        )

#LAYOUT
layout=html.Div([
                dbc.Row([
                        dbc.Col([
                                html.Label('Years Filter',className='label'),
                                slider ,                              
                                html.Label('Interactive map with available locations',className='label',style={"color":"red","margin-top":"3rem"}),
                                html.Label('Click me!',className='label',style={"color":"blue","font-size":"15px"}),
                                dcc.Graph(figure={},id="Map",clickData={'points': [{'customdata': 1}]},className='graph-map',style={"margin-top":"2rem"})
                                ],width={'size':6,'offset':0,'order':1},
                                xs={'size':12,'offset':0,'order':1}, 
                                sm={'size':12,'offset':0,'order':1}, 
                                md={'size':12,'offset':0,'order':1}, 
                                lg={'size':6,'offset':0,'order':1}, 
                                xl={'size':6,'offset':0,'order':1}
                                ),
                        dbc.Col([
                                dropList_Yvariable,
                                dcc.Graph(id="BoxPlot",figure={},className='graph',style={'height': '300px'}),
                                dcc.Graph(id="HeatMap",figure={},className='graph',style={'height': '300px'})
                                ],width={'size':6,'offset':0,'order':2},
                                xs={'size':12,'offset':0,'order':2}, 
                                sm={'size':12,'offset':0,'order':2}, 
                                md={'size':12,'offset':0,'order':1}, 
                                lg={'size':6,'offset':0,'order':2}, 
                                xl={'size':6,'offset':0,'order':2}
                                ),  
                        ]) ,
                html.Hr(),
                dbc.Row([
                        dbc.Col([
                                html.Label('Forecasting with SARIMA Model',className='label',style={"margin-top":"3rem","color":"blue"}),
                                html.Label('Number of months to forecast',className='label',style={"font-size":"15px","margin-top":"1rem"}),
                                slider2
                                ],width={'size':2},
                                xs={'size':12,'offset':0,'order':1}, 
                                sm={'size':12,'offset':0,'order':1}, 
                                md={'size':12,'offset':0,'order':1}, 
                                lg={'size':2,'offset':0,'order':1}, 
                                xl={'size':2,'offset':0,'order':1}
                                ),
                        dbc.Col([
                                dcc.Graph(id="Forecast",figure={},className='graph',style={'height': '300px'})
                                ],width={'size':6},style={"margin-top": "1rem"},
                                xs={'size':12,'offset':0,'order':2}, 
                                sm={'size':12,'offset':0,'order':2}, 
                                md={'size':12,'offset':0,'order':2}, 
                                lg={'size':6,'offset':0,'order':2}, 
                                xl={'size':6,'offset':0,'order':2}
                                ),
                        dbc.Col([             
                                dcc.Graph(id="Trend",figure={},className='graph',style={'height': '300px'})           
                                ],width={'size':4},style={"margin-top": "1rem"},
                                xs={'size':12,'offset':0,'order':3}, 
                                sm={'size':12,'offset':0,'order':3}, 
                                md={'size':12,'offset':0,'order':3}, 
                                lg={'size':4,'offset':0,'order':3}, 
                                xl={'size':4,'offset':0,'order':3}
                                )
                        ])                
        ])


#CALLBACKS

#call back for Map
@app.callback(
    Output(component_id='Map',component_property='figure'),
    Input(component_id='y-variable',component_property='value')
        )

def update_map(yvariable):
        #figure with the map
        fig_map = px.scatter_mapbox(df_locations, lat="Latitud", lon="Longitud", hover_name="Localization", 
                                color=yvariable,
                                size=yvariable, color_continuous_scale=px.colors.sequential.Bluered, size_max=40,
                                zoom=5, mapbox_style="open-street-map")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig_map.update_traces(customdata=df_locations['Localization'])

        return fig_map


#callback for boxplot
@app.callback(
    Output(component_id='BoxPlot',component_property='figure'),
    [Input(component_id='y-variable',component_property='value'),
    Input(component_id='my-range-slider',component_property='value'),
    Input(component_id='Map',component_property='clickData')]
)

def update_graph(variable,years,clickData):
        loc=clickData['points'][0]['customdata']

        dff=df[df['Localization']==loc]
        dff=dff[(dff['Year']>=years[0])&(dff['Year']<=years[1])]

        if variable=="DNI":
                ytitle="Irradiance (W/m^2)"
                range_values=[0,1100]
        elif variable=="Wind_Speed":
                ytitle="Wind Speed (m/s)"     
                range_values=[0,6]
        elif variable=="Temperature":
                ytitle="Temperature (°C)"   
                range_values=[20,40]                 

        BoxPlot_fig=px.box(dff,x='Month'  ,y=variable )
        BoxPlot_fig.update_layout(    
                margin=dict(l=0, r=0, t=0, b=0),
                template="plotly_white",
                yaxis_range=range_values,
                font=dict(
                        family="Lucida, sans-serif",
                        size=18,
                        color="black"),
                yaxis_title=ytitle ,        
                yaxis=dict(
                        titlefont_size=25,
                        tickfont_size=15),
                xaxis=dict(
                        titlefont_size=25,
                        tickfont_size=15),
                        )       

        return BoxPlot_fig



#callback for the Heatmap
@app.callback(
    Output(component_id='HeatMap',component_property='figure'),
    [Input(component_id='y-variable',component_property='value'),
    Input(component_id='my-range-slider',component_property='value'),
    Input(component_id='Map',component_property='clickData')]
)

def update_heatMap(variable,years,clickData):

        loc=clickData['points'][0]['customdata']
      
        dff=df[df['Localization']==loc]
        dff=dff[(dff['Year']>=years[0])&(dff['Year']<=years[1])]
        ala=pd.crosstab(dff['Month'],dff['Time'], values=dff[variable], aggfunc='mean')
        ala=ala.fillna(0)

        HeatMap_fig=px.imshow(ala)
        HeatMap_fig.update_layout(    
                margin=dict(l=0, r=0, t=0, b=0),
                template="plotly_white",
                font=dict(
                        family="Lucida, sans-serif",
                        size=18,
                        color="black"),
                yaxis_title='Month' ,   

                yaxis=dict(
                        titlefont_size=25,
                        tickfont_size=15),
                yaxis_nticks=12,
                xaxis=dict(
                        titlefont_size=25,
                        tickfont_size=13,
                        tickangle = 45),
                autosize = False
                        )  

        return HeatMap_fig



#call back for the forecast graphs
@app.callback(
    [Output(component_id='Forecast',component_property='figure'),
    Output(component_id='Trend',component_property='figure')],
    [Input(component_id='y-variable',component_property='value'),
    Input(component_id='my-slider',component_property='value'),
    Input(component_id='Map',component_property='clickData'), 
    ]
)

def update_graph(variable,periods,clickData):

    loc=clickData['points'][0]['customdata']

    dff = df.copy()
    dff = dff[dff['Localization']==loc]
    dff = dff.set_index('Fecha')
    dff = dff.resample('M').mean()

    components = seasonal_decompose(dff[variable], model='multiplicative')
    dff_trend = components.trend.reset_index().rename(columns={'trend':variable})
    mod = sm.tsa.statespace.SARIMAX(dff[variable], order=(0,1,1), seasonal_order=(1,1,1,12))
    SarimaModel = mod.fit()

    #because the slidebar:
    if periods==0:
        periods=1

    forecast = SarimaModel.get_forecast(steps=periods)
    predict=SarimaModel.predict()

    yhat = forecast.predicted_mean
    yhat_conf_int = forecast.conf_int(alpha=0.05)

    # make series for plotting purpose
    lower_series = pd.Series(yhat_conf_int.iloc[:,0])
    upper_series = pd.Series(yhat_conf_int.iloc[:,1])

    if variable=="DNI":
                ytitle="Irradiance (W/m^2)"
                range_values=[0,800]

    elif variable=="Wind_Speed":
                ytitle="Wind Speed (m/s)"
                range_values=[0,6]
    elif variable=="Temperature":
                ytitle="Temperature (°C)"
                range_values=[20,35]
                
    # Observed Graph
    fig = go.Figure([
        go.Scatter(
            name='Observed',
            x=dff.index,
            y=dff[variable],
            mode='lines',
            line=dict(color='rgb(31, 119, 180)'),
        ),
        
        go.Scatter(
            name='Forecast',
            x=yhat.index,
            y=yhat,
            mode='lines',
            line=dict(color='red'),
        ),  

        go.Scatter(
            name='Predicted',
            x=predict.index,
            y=predict,
            mode='lines',
            line=dict(color='pink'),
        ),   
        
        go.Scatter(
            name='Upper Bound',
            x=yhat.index,
            y=lower_series,
            mode='lines',
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False
        ),
        go.Scatter(
            name='Lower Bound',
            x=yhat.index,
            y=upper_series,
            marker=dict(color="#444"),
            line=dict(width=0),
            mode='lines',
            fillcolor='rgba(68, 68, 68, 0.3)',
            fill='tonexty',
            showlegend=False
        )
    ])

    fig.update_layout(
                        margin=dict(l=0, r=0, t=50, b=0),
                        title='Observed component',
                        title_x=0.5,
                        template="plotly_white",
                        font=dict(
                                        family="Lucida, sans-serif",
                                        size=18,
                                        color="black"),
                        yaxis=dict(
                                        title=ytitle,
                                        titlefont_size=25,
                                        tickfont_size=15),
                        xaxis=dict(
                                        title="Date",
                                        titlefont_size=25,
                                        tickfont_size=15),
                        )  
        


    #Trend Graph    
    Trend_fig= px.line(dff_trend, x="Fecha", y=variable)
    Trend_fig.update_layout(
                        margin=dict(l=0, r=0, t=50, b=0),
                        title='Trend component',               
                        title_x=0.5,
                        template="plotly_white",
                        yaxis_range=range_values,               
                        font=dict(
                                        family="Lucida, sans-serif",
                                        size=18,
                                        color="black"),
                        yaxis=dict(
                                        title=ytitle,
                                        titlefont_size=25,
                                        tickfont_size=15),
                        xaxis=dict(
                                        title="Date",
                                        titlefont_size=25,
                                        tickfont_size=15),                         
                        )   

    return fig,Trend_fig