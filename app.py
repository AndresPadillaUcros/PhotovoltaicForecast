#######################################################
# Main APP definition.
#
# Dash Bootstrap Components used for main theme and better
# organization.
#######################################################

from dash import Dash
import dash_bootstrap_components as dbc



app = Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True, 
                 meta_tags=[{'name': 'viewport','content': 'width=device-width, initial-scale=1.0 , maximum-scale=1.2, minimum-scale=0.5'}]
                 )


server = app.server

