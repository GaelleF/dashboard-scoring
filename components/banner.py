import base64

from dash import html


encoded_image = base64.b64encode(
    open("assets/logo_pret-depenser.png", 'rb').read())


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H4("SCORING"),
                    html.H6("Dashboard interactif"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Img(id="logo", src='data:image/png;base64,{}'.format(encoded_image.decode())
                             ),
                ],
            ),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'margin': '10px', 'borderBottom': '1px solid white'}
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)
