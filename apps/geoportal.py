#REQUIREMENTS
import dash
from dash import dcc,html,Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from pvlib import pvsystem
import pathlib
from app import app


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

#LOAD DATAFRAMES
df= pd.read_excel(DATA_PATH.joinpath("DataSetLimpio.xlsx"))
df_locations=pd.read_excel(DATA_PATH.joinpath("df_locations.xlsx"))
df_consumos=pd.read_excel(DATA_PATH.joinpath("consumos.xlsx")) 
df_power=pd.read_excel(DATA_PATH.joinpath("df_power.xlsx"))


#OBJECTS

#Month buttons
button1= html.Button('January', id='btn-10', n_clicks=0,className='button-month  ')
button2= html.Button('February', id='btn-11', n_clicks=0,className='button-month ')
button3= html.Button('March', id='btn-12', n_clicks=0,className='button-month ')
button4= html.Button('April', id='btn-13', n_clicks=0,className='button-month ' )
button5= html.Button('May', id='btn-14', n_clicks=0,className='button-month')
button6= html.Button('June', id='btn-15', n_clicks=0,className='button-month')
button7= html.Button('July', id='btn-16', n_clicks=0,className='button-month')
button8= html.Button('August', id='btn-17', n_clicks=0,className='button-month')
button9= html.Button('September', id='btn-18', n_clicks=0,className='button-month')
button10= html.Button('October', id='btn-19', n_clicks=0,className='button-month')
button11= html.Button('November', id='btn-20', n_clicks=0,className='button-month')
button12=html.Button('December', id='btn-21', n_clicks=0,className='button-month') 

#drop menu with Years to average
dropListYears = dcc.Dropdown(id='panel-selected', 
                            options=[{'label':'m-Si 585W','value':'monoCristalino'},  {'label':'p-Si 430W','value':'poliCristalino'},  
                                    {'label':'HIT 450W','value':'HIT'},  {'label':'CIGS 360W','value':'CIGS'} ,  {'label':'CdTe 460W','value':'CdTe'}  ], 
                            value='monoCristalino',
                            clearable=False,
                            style={'margin':'auto', 'width':'10rem'}
                            )


#drop menu n_panels
inputNumberPanels = dcc.Input(id='input-on-submit', type='number',value=14,style={ 'width':'5rem'})


#paneles
monoCristalino = {
    'Name': 'JKM585M-7RL4-V',
    'Precio':260,
    'Pmax':585,
    'Area':2.734,
    'n':21.4,
    'T_NOCT': 42.4,
    'N_s': 78,
    'I_sc_ref': 13.91,
    'V_oc_ref': 53.42,
    'I_mp_ref': 13.23,
    'V_mp_ref': 44.22,
    'alpha_sc': 0.0067,
    'a_ref': 1.81,
    'I_L_ref': 13.91,
    'I_o_ref': 2.20e-011,
    'R_s': 0.22198,
    'R_sh_ref': 400,
    'EgRef': 1.121,
    'dEgdT':-0.0002677,
}

poliCristalino = {
    'Name': 'CS3W-430P SE',
    'Precio':240,
    'Pmax':430,
    'Area':2.209,
    'n':19.46,
    'T_NOCT': 42,
    'N_s': 72,
    'I_sc_ref': 11.32,
    'V_oc_ref': 48.4,
    'I_mp_ref': 10.78,
    'V_mp_ref': 39.9,
    'alpha_sc': 0.0057,
    'a_ref': 1.943,
    'I_L_ref': 11.32,
    'I_o_ref': 1.64e-10,
    'R_s': 0.23594,
    'R_sh_ref': 2500,
    'EgRef': 1.121,
    'dEgdT':-0.0002677,
}

HIT = {
    'Name': 'REC450AA 72',
    'Precio':280,
    'Pmax':450,
    'Area':2.117,
    'n':21.3,
    'T_NOCT': 42.4,
    'N_s': 72,
    'I_sc_ref': 10.55,
    'V_oc_ref': 53.1,
    'I_mp_ref': 9.879,
    'V_mp_ref': 45.64,
    'alpha_sc': 0.0042,
    'a_ref': 1.998,
    'I_L_ref': 10.55,
    'I_o_ref': 2.80e-11,
    'R_s': 0.1956,
    'R_sh_ref': 4000,
    'EgRef': 1.121,
    'dEgdT':-0.0002677,
}

CIGS = {
    'Name': 'CIGS-3600A1',
    'Precio':210,
    'Pmax':360,
    'Area':2.347,
    'n':15.37,
    'T_NOCT': 46,
    'N_s': 110,
    'I_sc_ref': 6.445,
    'V_oc_ref': 76.67,
    'I_mp_ref': 6,
    'V_mp_ref': 60,
    'alpha_sc': 0.0006,
    'a_ref': 2.3502,
    'I_L_ref': 6.445,
    'I_o_ref': 3.40e-9,
    'R_s': 0.95899,
    'R_sh_ref': 413,
    'EgRef': 1.010,
    'dEgdT':-0.00011,
}

CdTe = {
    'Name': 'FS-6460-PA',
    'Pmax':460,
    'Area':2.315,
    'n':18.28,
    'T_NOCT': 46,
    'N_s': 264,
    'I_sc_ref': 2.59,
    'V_oc_ref': 222.9,
    'I_mp_ref': 2.44,
    'V_mp_ref': 188.8,
    'alpha_sc': 0.0010,
    'a_ref': 2.20219,
    'I_L_ref': 2.59,
    'I_o_ref': 3e-12,
    'R_s': 3.758832,
    'R_sh_ref': 13200,
    'EgRef': 1.475,
    'dEgdT':-0.0003,
}

#functions
def Power(df, panel_string):

    if panel_string=='monoCristalino':
        panel=monoCristalino
    elif panel_string=='poliCristalino':
        panel=poliCristalino
    elif panel_string=='HIT':
        panel=HIT
    elif panel_string=='CIGS':
        panel=CIGS
    elif panel_string=='CdTe':
        panel=CdTe
    
    NOCT= panel['T_NOCT']
    df['Tpanel']= df['Temperature'] + (NOCT -20)*df['DNI']/800
    
    Temperatura=df['Tpanel']
    Irradiancia=df['DNI']
    
    conditions=pd.DataFrame( {'Tpanel':Temperatura,'DNI':Irradiancia}  )
    IL, I0, Rs, Rsh, nNsVth = pvsystem.calcparams_desoto(
                                                            conditions['DNI'],
                                                            conditions['Tpanel'],
                                                            alpha_sc=panel['alpha_sc'],
                                                            a_ref=panel['a_ref'],
                                                            I_L_ref=panel['I_L_ref'],
                                                            I_o_ref=panel['I_o_ref'],
                                                            R_sh_ref=panel['R_sh_ref'],
                                                            R_s=panel['R_s'],
                                                            EgRef=1.121,
                                                            dEgdT=-0.0002677
                                                            )
    curve_info = pvsystem.singlediode(
                                            photocurrent=IL,
                                            saturation_current=I0,
                                            resistance_series=Rs,
                                            resistance_shunt=Rsh,
                                            nNsVth=nNsVth,
                                            ivcurve_pnts=100,
                                            method='lambertw'
                                        )
        
    power=curve_info['p_mp']   
    df['Power']=power   
    return df


layout=html.Div([
                html.Div([  
                            button1, button2,button3,button4, button5,button6,button7,button8,button9,button10, button11, button12
                            ],className='d-flex flex-wrap justify-content-center buttons-month  mx-4 '
                        ),                    
                html.Div([
                            html.Div([
                                        html.Label('Input the number of photovoltaic modules: ',className='label2 '),               
                                        inputNumberPanels
                                    ],className='text-center mx-auto' ),
                            html.Div([
                                        html.Label('Select the PV panel ',className='label2'),
                                        dropListYears
                                    ],className='text-center mx-auto'),
                            html.Div([
                                        html.Label('Simulations are perfomed with the One diode model',className='label2'),
                                    ],className='text-center mx-auto')
                            ], className='d-flex flex-wrap justify-content-center'
                        ),
  
                html.Div([
                            html.Div([                  
                                    html.Label('Interactive map with available locations',className='label',style={"color":"red","margin-top":"3rem"}),
                                    html.Label('Click me!',className='label',style={"color":"blue","font-size":"15px"}),
                                    dcc.Graph(figure={},id="Map2",clickData={'points': [{'customdata': 1}]},className='graph-map',style={"margin-top":"2rem"}),
                                    ],className='col-sm-12 col-md-12 col-lg-6'),
                            html.Div([
                                    dcc.Graph(id="DemandCurve",figure={},className='graph',style={'height': '300px'}),
                                    dcc.Graph(id="ExportFig",figure={},className='graph',style={'height': '300px'})
                                    ],className='col-sm-12 col-md-12 col-lg-6') 
                            ], className='row'
                        ),                
],className='container-fluid')




#Callback Active button
@app.callback(
    [Output(f"btn-{i}", "className") for i in range(10,22)],
    [Input(f"btn-{i}", "n_clicks") for i in range(10, 22)],
)
def set_active(*args):
    ctx = dash.callback_context

    if not ctx.triggered or not any(args):
        return ["button-month" for _ in range(10,22)]

    # get id of triggering button
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    return [
        "button-month active" if button_id == f"btn-{i}" else "button-month" for i in range(10,22)
    ]


#Callback Mapa
@app.callback(
    Output(component_id='Map2',component_property='figure'),
    [Input('btn-10', 'n_clicks'),
    Input('btn-11', 'n_clicks'),
    Input('btn-12', 'n_clicks'),
    Input('btn-13', 'n_clicks'),
    Input('btn-14', 'n_clicks'),
    Input('btn-15', 'n_clicks'),
    Input('btn-16', 'n_clicks'),
    Input('btn-17', 'n_clicks'),
    Input('btn-18', 'n_clicks'),
    Input('btn-19', 'n_clicks'),
    Input('btn-20', 'n_clicks'),
    Input('btn-21', 'n_clicks')]
    )

def update_map2(btn1,btn2,btn3,btn4,btn5,btn6,btn7, btn8,btn9,btn10,btn11,btn12):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-10' in changed_id:
        month = 1
    elif 'btn-11' in changed_id:
        month = 2
    elif 'btn-12' in changed_id:
        month = 3
    elif 'btn-13' in changed_id:
        month = 4
    elif 'btn-14' in changed_id:
        month = 5
    elif 'btn-15' in changed_id:
        month = 6
    elif 'btn-16' in changed_id:
        month = 7
    elif 'btn-17' in changed_id:
        month = 8
    elif 'btn-18' in changed_id:
        month = 9
    elif 'btn-19' in changed_id:
        month = 10
    elif 'btn-20' in changed_id:
        month =11
    else:
        month =12 

    df_power1=df_power[df_power['Month']==month]

    #figure with the map
    fig_map = px.scatter_mapbox(df_power1, lat="Latitud", lon="Longitud", hover_name="Localization", 
                                color='Power(W)',
                                size='Power(W)', color_continuous_scale=px.colors.sequential.Bluered, size_max=40,
                                zoom=5, mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig_map.update_traces(customdata=df_locations['Localization'])

    return fig_map

@app.callback(
    [Output(component_id='DemandCurve',component_property='figure'),
     Output(component_id='ExportFig',component_property='figure')],
    [Input('btn-10', 'n_clicks'),
    Input('btn-11', 'n_clicks'),
    Input('btn-12', 'n_clicks'),
    Input('btn-13', 'n_clicks'),
    Input('btn-14', 'n_clicks'),
    Input('btn-15', 'n_clicks'),
    Input('btn-16', 'n_clicks'),
    Input('btn-17', 'n_clicks'),
    Input('btn-18', 'n_clicks'),
    Input('btn-19', 'n_clicks'),
    Input('btn-20', 'n_clicks'),
    Input('btn-21', 'n_clicks'),      
    Input(component_id='Map2',component_property='clickData'),
    Input(component_id='input-on-submit',component_property='value'),
    Input(component_id='panel-selected',component_property='value')]
    )


def update_graph(btn1,btn2,btn3,btn4,btn5,btn6,btn7, btn8,btn9,btn10,btn11,btn12,clickData,n_panels,panel):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-10' in changed_id:
        month = 1
    elif 'btn-11' in changed_id:
        month = 2
    elif 'btn-12' in changed_id:
        month = 3
    elif 'btn-13' in changed_id:
        month = 4
    elif 'btn-14' in changed_id:
        month = 5
    elif 'btn-15' in changed_id:
        month = 6
    elif 'btn-16' in changed_id:
        month = 7
    elif 'btn-17' in changed_id:
        month = 8
    elif 'btn-18' in changed_id:
        month = 9
    elif 'btn-19' in changed_id:
        month = 7
    elif 'btn-20' in changed_id:
        month =11
    else:
        month =12 

    
    
    loc=clickData['points'][0]['customdata']
    

    dff=df.copy()
    dff=dff[dff['Localization']==loc].reset_index().drop(columns={'index'})  
    dff['Hour']=dff['Fecha'].dt.hour

    dff=dff[dff['Month']==int(month)]
    

    dff=dff.groupby('Hour')[['DNI','Temperature']].mean().round(1).reset_index()   


    df_power=Power( dff,   panel)
    
    df_power['Power']=int(n_panels)*df_power['Power']/1000
    
    
    df_consumos2=df_consumos.groupby('Hour')['Total'].mean().reset_index()
    df_consumos2['Total']=df_consumos2['Total'].round(2)
    
    x=np.array(df_power['Hour'])
    y=np.array(df_power['Power'])

    x1=np.array(df_consumos2['Hour'])
    y1=np.array(df_consumos2['Total'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x1, y=y1, line_shape='spline',name='House demand (kWh)',fill='tozeroy'))
    fig.add_trace(go.Scatter(x=x, y=y, line_shape='spline',name='Power(kWh)',fill='tozeroy'))

    fig.update_layout(
        template="plotly_white",
        title="Required energy",
        title_x=0.5,
        yaxis_title="Energy (kWh)",
        
        font=dict(
            family="Lucida, sans-serif",
            size=18,
            color="Black"),
        xaxis=dict(
            title='Hour of the day',
            tickmode='linear'),
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-1,
            xanchor="right",
            x=0.8
            )          
        )

    df_consumos2['Power']=df_consumos2['Hour'].map(df_power.set_index('Hour')['Power']).round(3).fillna(0)
    df_consumos2['kWh']=df_consumos2['Power']-df_consumos2['Total'] 
    df_consumos2["Operation"] = np.where(df_consumos2["kWh"]>0, 'Export Energy', 'Buy Energy')
    
    
    
    fig2 = px.bar(df_consumos2 , x='Hour', y='kWh',color='Operation',color_discrete_sequence=["red", "green"])

    fig2.update_layout(
        template="plotly_white",
        title="Export of energy to the grid ",
        title_x=0.5,
        yaxis_title="Energy (kWh)",
    
        font=dict(
            family="Lucida, sans-serif",
            size=18,
            color="Black"),          
        xaxis=dict(
            title='Hour of the day',
            tickmode='linear') , 
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-1,
            xanchor="right",
            x=0.8
            )       
        )

    return fig,fig2

