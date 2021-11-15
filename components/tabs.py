
from dash import html
import dash_core_components as dcc


def build_tabs(children_1, children_2):
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                  id="app-tabs",
                  value="tab2",
                  className="custom-tabs",
                  children=[
                      dcc.Tab(
                          id="insight-tab",
                          label="Indicateurs",
                          value="tab1",
                          className="custom-tab",
                          selected_className="custom-tab--selected",
                          children=[children_1]
                      ),
                      dcc.Tab(
                          id="form-tab",
                          label="Scoring",
                          value="tab2",
                          className="custom-tab",
                          selected_className="custom-tab--selected",
                          children=[children_2]
                      ),
                  ],
            )
        ],
    )
