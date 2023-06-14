import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import geopandas as gpd
import plotly.graph_objects as go

from api import get_price_info, get_room

df = gpd.read_file('europe.geojson')

app = dash.Dash(__name__)
colors = ["#FF0000",
          "#00FF00",
          "#0000FF",
          "#FF00FF",
          "#FFFF00",
          "#00FFFF",
          "#FF9900",
          "#00FF99",
          "#0099FF"]
cities = ["Amsterdam", "Athens", "Barcelona", "Berlin", "Budapest", "Lisbon", "Paris", "Rome", "Vienna"]
city_color_map = dict(zip(cities, colors))

global CITY
CITY = "Amsterdam"

app.layout = html.Div(
    children=[
        html.Div(
            className='map-container',
            children=[
                dcc.Graph(
                    id='choropleth-map',
                    figure=go.Figure(
                        data=go.Scattermapbox(
                            lat=df.geometry.y,
                            lon=df.geometry.x,
                            mode='markers',
                            marker=dict(
                                size=10,
                                color=df['color'],

                            ),
                            text=cities,  # Add city names as labels
                            hoverinfo='text',
                        ),
                        layout=go.Layout(
                            mapbox=dict(
                                center=dict(lat=49, lon=10),
                                style='carto-darkmatter',
                                zoom=3,
                            ),
                            margin=dict(l=0, r=0, t=0, b=0),
                            showlegend=False,  # Disable legend
                        )
                    )
                )
            ],
            style={'display': 'flex', 'justify-content': 'center'}  # Adjust the width as desired
        ),
        html.Div(
            id="left-container",
            children=[
                html.Div(
                    id="selected-city",
                    children=[]
                ),
                html.Div(
                    id='other-content',
                    children=[
                        # GRAPHS SHOULD BE HERE
                    ]
                )
            ],
            style={"display": "flex", "flex-direction": "column", "width": "100%"}
        )
    ],
    style={'background-color': '#222222', 'padding': '20px', 'height': '93vh', "display": "flex"}
)


@app.callback(
    Output('selected-city', 'children'),
    [Input('choropleth-map', 'clickData')]
)
def update_selected_city(clickData):
    print(clickData)
    if clickData is not None:
        global CITY
        CITY = clickData['points'][0]['text']
        return html.H3(f"Selected City: {CITY}")
    else:
        return html.H3("No city selected")


@app.callback(
    Output('other-content', 'children'),
    [Input('choropleth-map', 'clickData')]
)
def get_graphs(clickData):
    if clickData is not None:
        global CITY
        CITY = clickData['points'][0]['text']
        price_distribution, avg_cleanliness, avg_guest_satisfaction = get_price_info(CITY)
        room_chart = get_room(CITY)
        print(avg_cleanliness, avg_guest_satisfaction)

        return [
            dcc.Graph(figure=price_distribution),
            dcc.Graph(figure=room_chart)
        ]
    else:
        return []

if __name__ == '__main__':
    app.run_server(debug=True)
