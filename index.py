#REQUIREMENTS
import dash_bootstrap_components as dbc
from dash import Input, Output,dcc,html
from app import app

#LOAD THE DIFFERENT TABS
from apps import sidebar_component, home,analytics,geoportal

content = html.Div(id="page-content", children=[], className="content_style")

# PLACE THE COMPONENTS IN THE LAYOUT
app.layout = dbc.Container([ 
    dcc.Location(id="url",refresh=False),
    sidebar_component.sidebar,
    content
    ],fluid=True)

#CALLBACKS
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == '/apps/analytics':
        return analytics.layout   
    elif pathname == '/apps/geoportal':
        return geoportal.layout   

#RUN APP
if __name__==('__main__'):
    app.run_server(port = 8052, debug=True,use_reloader=True)