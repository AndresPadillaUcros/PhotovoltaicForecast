import dash_bootstrap_components as dbc
from dash import Input, Output,dcc,html

#OBJECTS
DS4A_Img = html.Img(src="assets\logo.svg", id="ds4a-image", className="logo_ds4a") 
COL_Img = html.Img(src="assets\logo_colombia.png", id="col-image", className="logo_col") 

sidebar = dbc.Nav([
            dbc.Row([
                        dbc.Col([
                                    DS4A_Img,
                                    COL_Img
                                ],className='d-flex justify-content-center m-auto',
                                xs={'size':12,'offset':0,'order':1}, 
                                sm={'size':12,'offset':0,'order':1}, 
                                md={'size':3,'offset':0,'order':1}, 
                                lg={'size':3,'offset':0,'order':1}, 
                                xl={'size':3,'offset':0,'order':1}
                                ),                              
                                
                        dbc.Col([                            
                                    dbc.NavLink("Home", href="/", active="exact"),
                                    dbc.NavLink("Analytics", href="/apps/analytics", active="exact"),       
                                    dbc.NavLink("Geoportal", href="/apps/geoportal", active="exact") 
                                ],className='d-flex justify-content-center m-auto',
                                xs={'size':12,'offset':0,'order':2}, 
                                sm={'size':12,'offset':0,'order':2}, 
                                md={'size':6,'offset':3,'order':2}, 
                                lg={'size':4,'offset':5,'order':2}, 
                                xl={'size':4,'offset':5,'order':2}
                                )
                 ],className='gap')
            ],className="sidebar_style ", vertical=True, pills=True)