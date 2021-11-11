# formulaire
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

default_values = {
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


def build_form(values=default_values):
    return html.Form([
        html.Label([html.Div(['Type de prêt : '], style={'width': '250px'}), dcc.Dropdown(
            id='NAME_CONTRACT_TYPE',
            options=[
                {'label': 'prêt', 'value': 0},  # 'Cash loans'
                {'label': 'prêt renouvelable', 'value': 1},  # 'Revolving loans'
            ], value=default_values['name_contract_type'], style={'width': '200px'})], className='row'),
        html.Label([html.Div(['Sexe : '], style={'width': '250px'}), dcc.Dropdown(
            id='CODE_GENDER',
            options=[
                {'label': 'Homme', 'value': 1},  # M
                {'label': 'Femme', 'value': 0},  # F
            ], value=default_values['code_gender'], style={'width': '200px'})], className='row'),

        html.Label([html.Div(["Nombre d'enfants : "], style={'width': '250px'}), dcc.Input(
            id='CNT_CHILDREN', type='number', min=0, max=15, step=1, value=default_values['cnt_children'])], className='row'),

        html.Label([html.Div(["Age : "], style={'width': '250px'}), dcc.Input(
            id='AGE', type='number', min=18, max=100, step=1, value=default_values['age'])], className='row'),
        html.Label([html.Div(['Possède une voiture : '], style={'width': '250px'}), dcc.Dropdown(
            id='FLAG_OWN_CAR',
            options=[
                {'label': 'oui', 'value': 1},  # 'Y'
                {'label': 'non', 'value': 0},  # 'N'
            ], value=default_values['flag_own_car'], style={'width': '200px'})], className='row'),
        html.Label([html.Div(['Possède un logement : '], style={'width': '250px'}), dcc.Dropdown(
            id='FLAG_OWN_REALTY',
            options=[
                {'label': 'oui', 'value': 1},  # 'Y'
                {'label': 'non', 'value': 0},  # 'N'
            ], value=default_values['flag_own_realty'], style={'width': '200px'})], className='row'),

        html.Label([html.Div(['Montant du crédit : '], style={'width': '250px'}),
                    dcc.Input(id="AMT_CREDIT", type="number", min=0, step=1,
                              placeholder="montant crédit", value=default_values['amt_credit'])
                    ], className='row'),

        html.Label([html.Div(['Montant des revenus : '], style={'width': '250px'}),
                    dcc.Input(id="AMT_INCOME", type="number", min=0, step=1,
                              placeholder="montant revenus", value=default_values['amt_income'])
                    ], className='row'),

        html.Label([html.Div(['zone de risque de la région (avec villes) : '], style={'width': '250px'}), dcc.Dropdown(
            id='REGION_RATING_CLIENT_W_CITY',
            options=[
                {'label': 'zone 1', 'value': 1},
                {'label': 'zone 2', 'value': 2},
                {'label': 'zone 3', 'value': 3},
            ], value=default_values['region_rating'], style={'width': '200px'})], className='row'),
        html.Label([html.Div(['Status familial : '], style={'width': '250px'}), dcc.Dropdown(
            id='FAMILY_STATUS',
            options=[
                {'label': 'marié', 'value': 'Married'},
                {'label': 'mariage civil', 'value': 'Civil marriage'},
                {'label': 'séparé', 'value': 'Separated'},
                {'label': 'Célibataire', 'value': 'Single_not_married'},
                {'label': 'veuf', 'value': 'Widow'},
            ], value=default_values['family_status'], style={'width': '200px'})], className='row'),
        html.Label([html.Div(['Type de revenu : '], style={'width': '250px'}), dcc.Dropdown(
            id='NAME_INCOME_TYPE',
            options=[
                {'label': 'Pension', 'value': 'Pensioner'},
                {'label': 'commercial', 'value': 'Commercial associate'},
                {'label': 'public', 'value': 'State servant'},
                {'label': 'salarié', 'value': 'Working'},
            ], value=default_values['name_income_type'], style={'width': '200px'})], className='row'),
        html.Label([html.Div(['Logement actuel : '], style={'width': '250px'}), dcc.Dropdown(
            id='NAME_HOUSING_TYPE',
            options=[
                {'label': 'colocation', 'value': 'Co-op apartment'},
                {'label': 'propriétaire', 'value': 'House_apartment'},
                {'label': 'logement social', 'value': 'Municipal apartment'},
                {'label': 'logement salarié', 'value': 'Office apartment'},
                {'label': 'locataire', 'value': 'Rented apartment'},
                {'label': 'chez les parents', 'value': 'With parents'},

            ], value=default_values['name_housing_type'], style={'width': '200px'})], className='row'),
        html.Label([html.Div(["niveau d'éducation : "], style={'width': '250px'}), dcc.Dropdown(
            id='NAME_EDUCATION_TYPE',  # TO CHECK !!!
            options=[
                {'label': 'master', 'value': 'Higher education'},
                {'label': 'universitaire', 'value': 'Incomplete higher'},
                {'label': 'bac', 'value': 'Secondary_secondary_special'},
                {'label': 'lycée', 'value': 'Lower secondary'},
            ], value=default_values['name_education_type'], style={'width': '200px'})], className='row'),
        html.Label([html.Div(['Type emploi : '], style={'width': '250px'}), dcc.Dropdown(
            id='OCCUPATION_TYPE',
            options=[
                {'label': 'comptable', 'value': 'Accountants'},
                {'label': 'employé', 'value': 'Core staff'},
                {'label': 'conducteur', 'value': 'Drivers'},
                {'label': 'personnel hautement qualifié',
                    'value': 'High_skill_staff'},
                {'label': 'ouvrier', 'value': 'Laborers'},
                {'label': 'personnel peu qualifié', 'value': 'Low_skill_staff'},
                {'label': 'manager', 'value': 'Managers'},
                {'label': 'medecine', 'value': 'Medicine staff'},
                {'label': 'autres', 'value': 'Others'},
                {'label': 'vendeur', 'value': 'Sales staff'},
            ], value=default_values['occupation_type'], style={'width': '200px'})], className='row'),
        html.Label([html.Div(['Secteur emploi : '], style={'width': '250px'}), dcc.Dropdown(
            id='ORGANIZATION_TYPE',
            options=[
                {'label': 'agriculture', 'value': 'Agriculture'},
                {'label': 'business entity', 'value': 'Business_Entity'},
                {'label': 'construction', 'value': 'construction'},
                {'label': 'education', 'value': 'Education'},
                {'label': 'finance', 'value': 'Finance'},
                {'label': 'gouvernement', 'value': 'Government'},
                {'label': 'industrie', 'value': 'Industry'},
                {'label': 'officiel', 'value': 'Official'},
                {'label': 'autre', 'value': 'Other'},
                {'label': 'immobilier', 'value': 'Realty'},
                {'label': 'securité', 'value': 'Security'},
                {'label': 'entrepreneur', 'value': 'Self-employed'},
                {'label': 'tourisme-restauration', 'value': 'TourismFoodSector'},
                {'label': 'commerce', 'value': 'Trade'},
                {'label': 'Transport', 'value': 'Transport'},
            ], value=default_values['organization_type'], style={'width': '200px'})], className='row'),
    ],  id='form_container', style={'marginRight': '10px', 'marginLeft': '10px'})
