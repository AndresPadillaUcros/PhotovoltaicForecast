#REQUIREMENTS
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

#OBJECTS
Home_Img = html.Div(  children=[html.Img(src="assets\landscape.jpg", id="ds4a-image", className="home_img")] )

analytics_text="This tab shows some graphs about the behaviour of the Direct Normal Irradiance and Wind Speed through different locations, years, months and hours."

card = dbc.Card(
    dbc.CardBody([
            html.H4("DashBoard Description", className="card-title"),
            html.H6("Analytics", className="card-subtitle"),
            html.P(analytics_text, className="card-text card"),
            html.H6("Geoportal", className="card-subtitle"),
            html.P("This tab shows irradiance in differents parts ", className="card-text card"),
            html.H6("Forecasting", className="card-subtitle"),
            html.P("This tab shows the forecasting ", className="card-text card"),           
             ]),style={"width": "40rem"},
    )

#LAYOUT
layout=html.Div([
            dbc.Row([
                dbc.Col('Irradiance in Colombia',className='titulo')
                    ]),
            html.Hr(),
            dbc.Row([
                    dbc.Col(card),
                    dbc.Col(Home_Img)
              ])
        ]) 



