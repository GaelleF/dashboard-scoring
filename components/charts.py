
import pandas as pd
import plotly.express as px
import dash_core_components as dcc


def draw_scoring_explanation(lime):
    lime_df = pd.DataFrame(lime, columns=['variable', 'value'])
    print( 'LIME bar h', lime_df['variable'])
    return {
            "data": [
                {
                    "x": lime_df['value'],
                    "y": lime_df['variable'],
                    "type": "bar",
                    "orientation": 'h',
                    #"marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
          
                }
            ],
            "layout": {
                "margin": dict(l=250, r=20, t=20, b=20),
                "showlegend": False,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
                #"height": '50vh'
            },
        }
    return dcc.Graph(
        id="bar-lime-chart",
        figure={
            "data": [
                {
                    "x": lime_df['value'],
                    "y": lime_df['variable'],
                    "type": "bar",
                    "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
                }
            ],
            "layout": {
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
                #"height": '50vh'
            },
        })
    
    
    #return px.bar(lime_df, x="value", y="variable", orientation='h')


def draw_pie_old(data_application_train):
    return dcc.Graph(id='piechart',
                     figure=px.pie(data_application_train, values='nombre de prêts demandés',
                                   names='TARGET', title='Taux acceptation'), className="col-sm")  # , template='plotly_dark'


def draw_pie(data_application_train):
    num_0 = len(data_application_train[data_application_train['TARGET'] == 0])
    num_1 = len(data_application_train[data_application_train['TARGET'] == 1])
    print('O=', num_0, '      1=', num_1)
    return dcc.Graph(
        id="piechart",
        figure={
            "data": [
                {
                    "labels": ['prêt correctement remboursé', 'prêt avec difficulté de payment'],
                    "values": [num_0, num_1],
                    "type": "pie",
                    "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
                }
            ],
            "layout": {
                "margin": dict(l=20, r=20, t=20, b=20),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
                #"height": '50vh'
            },
        },
    )
