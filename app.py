import os
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
import numpy as np

import requests

from components.banner import build_banner, generate_section_banner
from components.form import build_form
from components.tabs import build_tabs
from components.charts import draw_pie, draw_scoring_explanation

from utils.utils import get_columns, application_train_test, scoring_result
#suppress_callback_exceptions = True
#app = JupyterDash(__name__, external_stylesheets=[dbc.themes.SLATE])
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.SLATE]
)
server = app.server

# https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-manufacture-spc-dashboard/app.py

app.title = 'dashboard scoring'

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
#df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "spc_data.csv")))

df = pd.read_csv('data/application_train.csv', nrows=None)
test_df = pd.read_csv('data/application_test.csv', nrows=None)
print("Train samples: {}, test samples: {}".format(len(df), len(test_df)))

data_application_train = df
data_application_train['nombre de prêts demandés'] = 1
data_application_train['prêt accepté'] = np.where(
    data_application_train['TARGET'] == 0, 'Oui', 'Non')

test_df=application_train_test(test_df)
list_for_dropdown = [{'label': id, 'value': id}
                     for id in test_df['SK_ID_CURR']]



app.layout = html.Div([
    build_banner(),
    html.Div(
        children=[
            build_tabs(
                children_1=html.Div([
                  html.Div([
                    html.Div([generate_section_banner('Taux acceptation'),
                              draw_pie(data_application_train), ],
                             id="ooc-piechart-outer",
                             style={ 'width': '46vw'},
                             className='cards-graph'),
                    html.Div([
                        generate_section_banner(
                            html.Label(["Variable à visualiser :",
                                        dcc.Dropdown(
                                            id='variable-dropdown', clearable=False,
                                            value='CODE_GENDER', options=[
                                                {'label': c, 'value': c}
                                                for c in get_columns(data_application_train)],  style={'width': '200px'})
                                        ],
                                        style={'display': 'flex', 'justifyContent': 'space-around', 'width': '90%', 'align-items':'center'})),
                        html.Div(id='graph', style={'height': '50vh'})
                    ], style={  'width': '46vw'}, 
                    className='cards-graph'),  # style={'display':'flex', 'justifyContent': 'space-around', 'height':'100%'}) ,
                ], className='row', style={'display': 'flex', 'justifyContent': 'center'})],
                className='container-fluid'),
                children_2=html.Div([
                    html.Div([
                        generate_section_banner(html.Div([
                          html.H6('Formulaire demande de prêt'), #, style={'width': '400px', 'display': 'flex'}
                          dcc.Dropdown(id='SELECT_CLIENT_TEST',
                              options=list_for_dropdown, placeholder='Selectionner un client', style={'width': '200px'})
                        ], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '95%',
                        'align-items':'center'})
                                 ), # ], style={'display': 'flex'}, className="four column")
                        build_form()], className="col-sm cards-graph",),  # id='build_form'
                    html.Div([
                      generate_section_banner(html.Div([
                        html.H6('Résulats scoring'),
                        html.Button('Mettre à jour le scoring',
                                          id='submit-scoring'),
                      ],
                       style={'display': 'flex', 'justifyContent': 'space-around', 'width': '90%',
                       'align-items':'center'})),
                     html.Div([
                                  html.Div(id='scoring_result', style={'font-size': '2rem'}),
                                  #dcc.Graph(id='scoring_explanation'),
                                  dcc.Loading(id = "loading-icon",
                           #'graph', 'cube', 'circle', 'dot', or 'default'
                 type = 'cube',
                children=[html.Div(dcc.Graph(id='scoring_explanation'),
                  style={'display': 'None'}, id='scoring_explanation_container')])
                              ], id='container-scoring')], className="col-sm cards-graph")
                ], className='row')
            ),
        ],
        id="app-container"
    ),
], id="big-app-container ")


# Define callback to update graph
@app.callback(
    Output('graph', 'children'),
    [Input("variable-dropdown", "value")]
)
def update_figure(variable):
    df_pivot = pd.pivot_table(data_application_train, values='nombre de prêts demandés', columns=[
                              variable, 'prêt accepté'], aggfunc='count').T.reset_index()
    df_pivot_0=df_pivot[df_pivot['prêt accepté']=='Oui']
    df_pivot_1=df_pivot[df_pivot['prêt accepté']=='Non']

    return dcc.Graph(
        id="bar_variable",
        figure={
            "data": [
                {
                    "x": df_pivot_0[variable],
                    "y": df_pivot_0['nombre de prêts demandés'],
                    "type": "bar",
                    # "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
                    "name":"prêt remboursé",
                },
                {
                    "x": df_pivot_1[variable],
                    "y": df_pivot_1['nombre de prêts demandés'],
                    "color": df_pivot_1['prêt accepté'],
                    "type": "bar",
                    # "marker": {"line": {"color": "white", "width": 1}},
                    "hoverinfo": "label",
                    "textinfo": "label",
                    "name": 'Prêt avec difficulté de paiement'
                }

            ],
            "layout": {
                #"padding": dict(l=30, r=20, t=20, b=100),
                "margin": dict(l=40, r=20, t=20, b=100),
                "showlegend": True,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "font": {"color": "white"},
                "autosize": True,
            },
        },
         style={'height': '100%', 'max-width': '100%'}
    )



def hot_deencoding(data_dict, variable_name):
    for k, v in data_dict.items():
        if ((k.startswith(variable_name)) & (v == 1)):
            return k.replace(variable_name, '')

# Define callback for choosen test client


@app.callback(
    [Output('NAME_CONTRACT_TYPE', 'value'), Output('CODE_GENDER', 'value'),
     Output('CNT_CHILDREN', 'value'), Output('AGE', 'value'),
     Output('FLAG_OWN_CAR', 'value'), Output('FLAG_OWN_REALTY', 'value'),
     Output('AMT_CREDIT', 'value'), Output('AMT_INCOME', 'value'),
     Output('REGION_RATING_CLIENT_W_CITY', 'value'), Output(
         'FAMILY_STATUS', 'value'),
     Output('NAME_INCOME_TYPE', 'value'), Output('NAME_HOUSING_TYPE', 'value'),
     Output('NAME_EDUCATION_TYPE', 'value'), Output(
         'OCCUPATION_TYPE', 'value'),
     Output('ORGANIZATION_TYPE', 'value'),
     ],
    [Input("SELECT_CLIENT_TEST", "value")]
)
def get_test_data(client_test):
    # valeur par défaut
    values = {
        'name_contract_type': 0,
        'code_gender': 0,
        'cnt_children': 0,
        'age': 18,
        'flag_own_car': 0,
        'flag_own_realty': 0,
        'amt_credit': 1,
        'amt_income': 1,
        'region_rating': 1,
        'family_status': 'Married',
        'name_income_type': 'Pensioner',
        'name_housing_type': 'Rented apartment',
        'name_education_type': 'Lower secondary',
        'occupation_type': 'Low_skill_staff',
        'organization_type': 'Agriculture'
    }

    if client_test != None:
        data_client = test_df[test_df['SK_ID_CURR'] == client_test].to_dict('records')[
            0]
        family_status = hot_deencoding(data_client, 'NAME_FAMILY_STATUS_')
        name_income = hot_deencoding(data_client, 'NAME_INCOME_TYPE_')
        name_housing = hot_deencoding(data_client, 'NAME_HOUSING_TYPE_')
        name_education = hot_deencoding(data_client, 'NAME_EDUCATION_TYPE_')
        occupation_type = hot_deencoding(data_client, 'OCCUPATION_TYPE_')
        organization_type = hot_deencoding(data_client, 'ORGANIZATION_TYPE_')

        values = {
            'name_contract_type': data_client['NAME_CONTRACT_TYPE'],
            'code_gender': data_client['CODE_GENDER'],
            'cnt_children': data_client['CNT_CHILDREN'],
            'age': data_client['AGE'],
            'flag_own_car': data_client['FLAG_OWN_CAR'],
            'flag_own_realty': data_client['FLAG_OWN_REALTY'],
            'amt_credit': data_client['AMT_CREDIT'],
            'amt_income': data_client['AMT_INCOME_TOTAL'],
            'region_rating': data_client['REGION_RATING_CLIENT_W_CITY'],
            'family_status': family_status,
            'name_income_type': name_income,
            'name_housing_type': name_housing,
            'name_education_type': name_education,
            'occupation_type': occupation_type,
            'organization_type': organization_type
        }
        print(values)
        print('RERE', values['code_gender'], values['name_contract_type'],
              )
    return [values['name_contract_type'], values['code_gender'], values['cnt_children'],
            values['age'],
            values['flag_own_car'],
            values['flag_own_realty'],
            values['amt_credit'],
            values['amt_income'],
            values['region_rating'],
            values['family_status'],
            values['name_income_type'],
            values['name_housing_type'],
            values['name_education_type'],
            values['occupation_type'],
            values['organization_type']]


# Define callback to show scoring and explanation (LIME) from flask API
@app.callback(
    Output('scoring_result', 'children'),
    Output('scoring_explanation', 'figure'),
    Output('scoring_explanation_container', 'style'),
    [Input("submit-scoring", "n_clicks")],
    [
        State("NAME_CONTRACT_TYPE", "value"),
        State('CODE_GENDER', "value"),
        State('CNT_CHILDREN', "value"),
        State('AGE', "value"),
        State('FLAG_OWN_CAR', "value"),
        State('FLAG_OWN_REALTY', "value"),
        State("AMT_CREDIT", "value"),
        State("AMT_INCOME", "value"),
        State('REGION_RATING_CLIENT_W_CITY', "value"),
        State('FAMILY_STATUS', "value"),
        State('NAME_INCOME_TYPE', "value"),
        State('NAME_EDUCATION_TYPE', "value"),
        State('OCCUPATION_TYPE', "value"),
        State('ORGANIZATION_TYPE', "value"),
        State('NAME_HOUSING_TYPE', "value"),
    ])
def ask_scoring(n_clicks, name_contract_type, code_gender, cnt_children, age, flag_own_car, flag_own_realty,
                amt_credit, amt_income, region_rating, family_status, name_income_type, name_education_type,
                occupation_type, organization_type, housing_type):
    print('click', name_contract_type, code_gender, cnt_children, age, flag_own_car, flag_own_realty,
          amt_credit, amt_income, region_rating, family_status, name_income_type, name_education_type,
          occupation_type, organization_type)
    ratio = amt_income/amt_credit
    amt_credit= np.log(amt_credit)
    amt_income= np.log(amt_income)
    payload = {"NAME_CONTRACT_TYPE": name_contract_type, "CODE_GENDER": code_gender, "FLAG_OWN_CAR": flag_own_car,
               "FLAG_OWN_REALTY": flag_own_realty, "CNT_CHILDREN": cnt_children, "AMT_INCOME_TOTAL": amt_income,
               "AMT_CREDIT": amt_credit, "REGION_RATING_CLIENT_W_CITY": region_rating,
               "NEW_INCOME_CREDIT_RATIO": ratio,
               "NAME_INCOME_TYPE_Commercial associate": 0.0, "NAME_INCOME_TYPE_Pensioner": 0.0,
               "NAME_INCOME_TYPE_State servant": 0.0, "NAME_INCOME_TYPE_Working": 0.0,


                "NAME_EDUCATION_TYPE_Higher education":0,"NAME_EDUCATION_TYPE_Incomplete higher":0,
                "NAME_EDUCATION_TYPE_Lower secondary":0,"NAME_EDUCATION_TYPE_Secondary_secondary_special": 0.0,

               "NAME_FAMILY_STATUS_Civil marriage": 0.0, "NAME_FAMILY_STATUS_Married": 0.0,
               "NAME_FAMILY_STATUS_Separated": 0.0, "NAME_FAMILY_STATUS_Single_not_married": 0.0,
               "NAME_FAMILY_STATUS_Widow": 0.0,

               "NAME_HOUSING_TYPE_Co-op apartment": 0.0, "NAME_HOUSING_TYPE_House_apartment": 0.0,
               "NAME_HOUSING_TYPE_Municipal apartment": 0.0, "NAME_HOUSING_TYPE_Office apartment": 0.0,
               "NAME_HOUSING_TYPE_Rented apartment": 0.0, "NAME_HOUSING_TYPE_With parents": 0.0,

               "OCCUPATION_TYPE_Accountants": 0.0, "OCCUPATION_TYPE_Core staff": 0.0, "OCCUPATION_TYPE_Drivers": 0.0,
               "OCCUPATION_TYPE_High_skill_staff": 0.0, "OCCUPATION_TYPE_Laborers": 0.0,
               "OCCUPATION_TYPE_Low_skill_staff": 0.0, "OCCUPATION_TYPE_Managers": 0.0,
               "OCCUPATION_TYPE_Medicine staff": 0.0, "OCCUPATION_TYPE_Others": 0.0,
               "OCCUPATION_TYPE_Sales staff": 0.0,

               "ORGANIZATION_TYPE_Agriculture": 0.0,
               "ORGANIZATION_TYPE_Business_Entity": 0.0, "ORGANIZATION_TYPE_Construction": 0.0,
               "ORGANIZATION_TYPE_Education": 0.0, "ORGANIZATION_TYPE_Finance": 0.0,
               "ORGANIZATION_TYPE_Government": 0.0, "ORGANIZATION_TYPE_Industry": 0.0,
               "ORGANIZATION_TYPE_Official": 0.0, "ORGANIZATION_TYPE_Other": 0.0, "ORGANIZATION_TYPE_Realty": 0.0,
               "ORGANIZATION_TYPE_Security": 0.0, "ORGANIZATION_TYPE_Self-employed": 0.0,
               "ORGANIZATION_TYPE_TourismFoodSector": 0.0, "ORGANIZATION_TYPE_Trade": 0.0,
               "ORGANIZATION_TYPE_Transport": 0.0, "ORGANIZATION_TYPE_XNA": 0.0,

               "NEW_SEGMENT_AGE_Middle_Age": 0.0, "NEW_SEGMENT_AGE_Old": 0.0, "NEW_SEGMENT_AGE_Young": 0.0,

               "NEW_SEGMENT_INCOME_High_Income": 0.0, "NEW_SEGMENT_INCOME_Low_Income": 0.0,
               "NEW_SEGMENT_INCOME_Middle_Income": 0.0}


    if (name_income_type != None):
      payload["NAME_INCOME_TYPE_"+name_income_type] = 1
    if (name_education_type != None):
      payload["NAME_EDUCATION_TYPE_"+name_education_type]=1
    if (family_status != None):
      payload["NAME_FAMILY_STATUS_"+family_status] = 1
    if (housing_type != None):
      payload["NAME_HOUSING_TYPE_"+housing_type] = 1
    if (occupation_type != None):
      payload["OCCUPATION_TYPE_"+occupation_type] = 1
    if (organization_type != None):
      payload["ORGANIZATION_TYPE_"+organization_type] = 1

    if amt_income <= 112500:
        payload["NEW_SEGMENT_INCOME_Low_Income"] = 1
    elif amt_income <= 225000:
        payload["NEW_SEGMENT_INCOME_Middle_Income"] = 1
    else:
        payload["NEW_SEGMENT_INCOME_High_Income"] = 1

    if age <= 34:
        payload["NEW_SEGMENT_AGE_Young"] = 1
    elif age <= 54:
        payload["NEW_SEGMENT_AGE_Middle_Age"] = 1
    else:
        payload["NEW_SEGMENT_AGE_Old"] = 1

    print(payload)
    if n_clicks is None:
        raise PreventUpdate
    # "http://localhost:5000/predict/"
    scoring_requests = requests.post(
        "https://scoring-oc-server.herokuapp.com/predict", data=payload)

    json_data = scoring_requests.json()
    #response = pd.DataFrame(json_data)
    print(json_data, json_data['lime'])
    return scoring_result(json_data['target']), draw_scoring_explanation(json_data['lime']),{'display': 'block'}


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
    #app.run(debug=True)
