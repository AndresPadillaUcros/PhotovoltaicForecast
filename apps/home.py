#REQUIREMENTS
from dash import html
import dash_bootstrap_components as dbc

#OBJECTS
Home_Img = html.Img(src="assets\landscape.jpg", id="ds4a-image", className="home_img")

analytics_text="This tab shows some graphs about the behaviour of the Direct Normal Irradiance, temperatura and Wind Speed through different locations, years, months and hours. This also shows the forecasting of the previous variables using the Sarima model"
geoportal_text="This tab shows the power generated using different photovoltaic modules though different locations, showing the amount of energy that can be exported to the grid"

card = dbc.Card(
    dbc.CardBody([
            html.H4("DashBoard Description", className="card-title"),
            html.H6("Analytics", className="card-subtitle"),
            html.P(analytics_text, className="card-text card"),
            html.H6("Geoportal", className="card-subtitle"),
            html.P(geoportal_text, className="card-text card"),   
             ]),style={'width':'50rem','margin':'auto'},
    )

#LAYOUT
layout=html.Div([
            html.Div([
                html.Div('Irradiance in Colombia',className='titulo ')
                    ]),
            html.Hr(),
            html.Div([
                        card,
                        Home_Img
                    ],className='d-flex flex-wrap justify-content-center')
        ]) 



