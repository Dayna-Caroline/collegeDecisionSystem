import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import backend

# Carregar dados de mesorregiões
mesorregioes = backend.get_mesorregioes()
mesorregiao_options = [{"label": m["nome"], "value": m["nome"]} for m in mesorregioes]

# Carregar dados do arquivo para determinar as faixas de concorrência
def carregar_opcoes_concorrencia():
    faixa_concorrencia = [
        {"label": "1-5 concorrentes", "value": "1-5"},
        {"label": "6-10 concorrentes", "value": "6-10"},
        {"label": "11-20 concorrentes", "value": "11-20"},
        {"label": "21-50 concorrentes", "value": "21-50"},
        {"label": "51+ concorrentes", "value": "51+"}
    ]
    return faixa_concorrencia

faixa_concorrencia_options = carregar_opcoes_concorrencia()

# Inicialização do app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.P("Tomada de Decisão - Faculdade", style={"color": "white", "font-weight": "700"}),
            html.P("Utilize este dashboard para definir o melhor município e os 10 melhores cursos de cada mesorregião para abrir sua faculdade.", 
                   style={"color": "lightgray", "font-size": "12px", "text-align": "justify"}),

            # Filtro de Mesorregião
            html.Label("Mesorregião", style={"color": "white", "font-size": "14px", "font-weight": "700"}),
            dcc.Dropdown(id="mesorregiao-dropdown", options=mesorregiao_options, value=mesorregioes[0]["nome"], 
                         style={"background-color": "#333", "color": "white", "border": "none", "font-size": "14px"},
                         placeholder="Selecione a Mesorregião",
                         className="dropdown-dark"),

            # Filtro de Faixa de Concorrentes
            html.Label("Faixa de Concorrentes", style={"color": "white", "margin-top": "5px", "font-size": "14px", "font-weight": "700"}),
            dcc.Dropdown(id="concorrentes-dropdown", options=faixa_concorrencia_options, value=faixa_concorrencia_options[0]["value"], 
                         style={"background-color": "#333", "color": "white", "border": "none", "font-size": "14px"},
                         placeholder="Selecione a Faixa de Concorrentes",
                         className="dropdown-dark"),

            # Cursos Recomendados
            html.H3("Cursos Recomendados", style={"color": "white", "margin-top": "20px", "font-size": "14px", "font-weight": "700"}),
            html.Div(id="cursos-lista", style={"font-size": "12px", "color": "lightgray"})
        ], width=5, style={"background-color": "#1a1a1a", "padding": "15px", "height": "100vh", "overflow": "hidden"}),

        dbc.Col([
            html.Iframe(id="mapa-mesorregiao", style={"width": "100%", "height": "100vh", "border": "none", "display": "block"})
        ], width=7, style={"background-color": "#333", "padding": "0", "height": "100vh"})
    ], style={"width": "100%", "margin": "0", "height": "100vh"})
], fluid=True, style={"padding": "0", "margin": "0", "width": "100vw", "max-width": "100vw", "height": "100vh"})

# Callback para atualizar o mapa e a lista de cursos
@app.callback(
    [Output("mapa-mesorregiao", "srcDoc"),
     Output("cursos-lista", "children")],
    [Input("mesorregiao-dropdown", "value"),
     Input("concorrentes-dropdown", "value")]
)
def update_output(mesorregiao_nome, concorrentes_faixa):
    # Obter o ID da mesorregião selecionada
    mesorregiao_id = next((m["id"] for m in mesorregioes if m["nome"] == mesorregiao_nome), None)
    
    # Extrair min e max da faixa de concorrentes
    if concorrentes_faixa == "51+":
        min_concorrentes, max_concorrentes = 51, float("inf")
    else:
        min_concorrentes, max_concorrentes = map(int, concorrentes_faixa.split("-"))

    # Buscar município com menos concorrentes na faixa
    municipio_nome = backend.get_municipio_com_menos_concorrentes(mesorregiao_id, min_concorrentes, max_concorrentes)
    
    if municipio_nome is None:
        return "", html.P("Não foi possível encontrar um município com o número especificado de concorrentes.", style={"color": "lightgray"})
    
    latitude, longitude = backend.get_lat_lon(municipio_nome)
    if latitude is None or longitude is None:
        return "", html.P("Não foi possível obter os dados de localização.", style={"color": "lightgray"})
    
    mapa_html = backend.gerar_mapa_html(mesorregiao_nome, municipio_nome, latitude, longitude, mesorregiao_id)
    
    cursos_lista = backend.get_cursos_recomendados(mesorregiao_id)
    cursos_table = dbc.Table(
        [html.Tbody([html.Tr([html.Td(curso, style={"border": "1px solid black", "color": "lightgray"})]) for curso in cursos_lista])],
        bordered=False,
        dark=True,
        striped=False,
        hover=True,
        style={"width": "100%", "margin-top": "5px"}
    )

    return mapa_html, cursos_table

# Executar o app
if __name__ == "__main__":
    app.run_server(debug=True)
