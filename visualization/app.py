import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import dash_daq as daq
import plotly.express as px
import networkx as nx

import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

from collections import Counter


import chart_studio.plotly as py
import plotly.figure_factory as ff

from wordcloud import WordCloud

import json


app = dash.Dash()
app.css.append_css({"external_url" : "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv('movies_for_vis.csv', encoding='latin1')
df = df.dropna()

def lang_pop(num):

    unique = list(df.original_language.unique())
    list_ratio=[]
    for each in unique:
        x = df[df["original_language"] == each]
        ratio_popularity = sum(x.popularity)/len(x)
        list_ratio.append(ratio_popularity)

    df2 = pd.DataFrame({"language":unique,"ratio":list_ratio})
    new_index = (df2.ratio.sort_values(ascending = False)).index.values
    sorted_data= df2.reindex(new_index).iloc[:num]

    trace1 = go.Bar(
    x = sorted_data.language,
    y = sorted_data.ratio,
    name = "Ratio",
    marker = dict(
            color = list(range(1, 35)),
            colorscale = "Bluered")
    )

    data1= [trace1]
    layout = dict(barmode = "group", 
                  title='plotly langugare popularity plot',
                 xaxis =  dict(title_text='language',showgrid = False, showline = False, zeroline = False),
              yaxis = dict(title_text='popularity', showgrid = False, showline = False, zeroline = False))

    fig = go.Figure(data=data1, layout=layout)
    
    return fig

def line_runtime_pop(num):
    df1 = df.head(num).copy()

    trace1 =go.Scatter(
        x =df1.index,
        y = df1.popularity,
        mode ="lines",
        name = " Popularity",
        marker = dict(color = "rgb(242, 99, 74,0.7)"),
        text = df1.original_title
    )
    trace2 = go.Scatter(
        x = df1.index,
        y = df1.runtime,
        mode = "lines + markers",
        name = "Runtime",
        marker = dict( color = "rgb(144, 211, 74,0.5)"),
        text = df1.original_title
    )
    trace3 = go.Scatter(
        x = df1.index,
        y = df1.vote_average,
        mode = "markers",
        name = "Vote Averge",
        marker = dict(color = "rgb(118, 144, 165)"),
        text = df1.original_title
    )
    data1=[trace1,trace2,trace3]
    layout = dict(
        title = "Runtime vs Popularity"
    )
    fig = go.Figure(data=data1, layout=layout)
    return fig

def pie_production(level):
    a=[]
    for each in df.production_countries.str.split("|"):
        for i in each:
            a.append(i)

    b = dict(Counter(a))

    keys=[]
    values=[]

    for key,value in b.items() :
        if value > level and key != "":
            keys.append(key)
            values.append(value)

    labels = keys
    sizes= values

    aaa = pd.DataFrame({'country': labels, 'pop': sizes})

    fig = px.pie(aaa, values='pop', names='country', title='production countries')

    return fig


app.layout = html.Div([
        html.H1("exam app"),
        html.H2("This project is dash app showing plots concerning movies dataset relaesed by IMDB"),


        dcc.Slider(id='plot_option', min=1, max=100, step=1, value=10,),
        html.Div([html.Div(dcc.Graph(id = "figure_"))], className = "row"),

        dcc.Slider(id='line_plot', min=10, max=30000, step=1, value=100,),
        html.Div([html.Div(dcc.Graph(id = "figure_line"))], className = "row"),

        dcc.Slider(id='pie_plot', min=10, max=10000, step=1, value=1000,),
        html.Div([html.Div(dcc.Graph(id = "figure_pie"))], className = "row"),



        ], className = "container")

@app.callback(
        Output(component_id = "figure_", component_property = "figure"),
        [Input(component_id = "plot_option", component_property = "value")]
        )
def update_graph(value):
    return lang_pop(value)

@app.callback(
        Output(component_id = "figure_line", component_property = "figure"),
        [Input(component_id = "line_plot", component_property = "value")]
        )
def update_graph(value):
    return line_runtime_pop(value)

@app.callback(
        Output(component_id = "figure_pie", component_property = "figure"),
        [Input(component_id = "pie_plot", component_property = "value")]
        )
def update_graph(value):
    return pie_production(value)


if __name__ == "__main__":
        app.run_server(debug = True)


