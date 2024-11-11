import pandas as pd
import folium
from opencage.geocoder import OpenCageGeocode
import requests
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações de API e geocodificador
OPENCAGE_API_KEY = os.getenv("API_KEY")
geocoder = OpenCageGeocode(OPENCAGE_API_KEY)

def get_mesorregioes():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/mesorregioes"
    response = requests.get(url)
    return response.json()

def get_municipios_by_mesorregiao(mesorregiao_id):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes/{mesorregiao_id}/municipios"
    response = requests.get(url)
    return response.json()

def get_geojson_mesorregiao(mesorregiao_id):
    url = f"https://servicodados.ibge.gov.br/api/v2/malhas/{mesorregiao_id}?formato=application/vnd.geo+json"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def get_municipio_com_menos_concorrentes(mesorregiao_id, min_concorrentes, max_concorrentes):
    faculdades_data = pd.read_csv("data/MEC - dadosFaculdadesSPAtivas2022.csv", delimiter=",")
    municipios = get_municipios_by_mesorregiao(mesorregiao_id)
    codigos_municipios = [municipio["id"] for municipio in municipios]

    faculdades_mesorregiao = faculdades_data[faculdades_data["CODIGO_MUNICIPIO_IBGE"].isin(codigos_municipios)]
    faculdades_contagem = faculdades_mesorregiao.groupby("CODIGO_MUNICIPIO_IBGE").size().reset_index(name="CONCORRENTES")

    faculdades_contagem_filtrada = faculdades_contagem[
        (faculdades_contagem["CONCORRENTES"] >= min_concorrentes) & 
        (faculdades_contagem["CONCORRENTES"] <= max_concorrentes)
    ]
    
    if not faculdades_contagem_filtrada.empty:
        municipio_escolhido = faculdades_contagem_filtrada.sort_values("CONCORRENTES").iloc[0]["CODIGO_MUNICIPIO_IBGE"]
        municipio_nome = next((m["nome"] for m in municipios if m["id"] == municipio_escolhido), None)
        return municipio_nome
    else:
        return None

def get_cursos_recomendados(mesorregiao_id):
    cursos_data = pd.read_csv("data/MEC - dadosCursosSP2022.csv", delimiter=",")
    municipios = get_municipios_by_mesorregiao(mesorregiao_id)
    codigos_municipios = [municipio["id"] for municipio in municipios]
    
    cursos_mesorregiao = cursos_data[cursos_data["CODIGO_MUNICIPIO"].isin(codigos_municipios)]
    top_cursos = cursos_mesorregiao.drop_duplicates(subset=["NOME_CURSO"])
    top_cursos = top_cursos.sort_values(by="QT_VAGAS_AUTORIZADAS", ascending=False).head(10)
    top_cursos = top_cursos.sort_values(by="NOME_CURSO")
    
    return top_cursos["NOME_CURSO"].tolist()

def gerar_mapa_html(mesorregiao_nome, municipio_nome, latitude, longitude, mesorregiao_id):
    mapa = folium.Map(location=[latitude, longitude], zoom_start=10)
    geojson_data = get_geojson_mesorregiao(mesorregiao_id)
    if geojson_data:
        folium.GeoJson(
            geojson_data,
            name="Mesorregião",
            style_function=lambda x: {"color": "blue", "weight": 2, "fillOpacity": 0.1},
            highlight_function=lambda x: {"color": "red", "weight": 3}
        ).add_to(mapa)
    
    folium.Marker(
        [latitude, longitude],
        popup=f"{municipio_nome}, {mesorregiao_nome}",
        icon=folium.Icon(color="blue")
    ).add_to(mapa)

    folium.map.Marker(
        [latitude, longitude],
        icon=folium.DivIcon(
            html=f"""<div style="font-size: 10pt; color: black">
                     <b>{municipio_nome}</b> - {mesorregiao_nome}</div>"""
        ),
    ).add_to(mapa)

    map_data = BytesIO()
    mapa.save(map_data, close_file=False)
    return map_data.getvalue().decode("utf-8")

def get_lat_lon(municipio_nome):
    query = f"{municipio_nome}, São Paulo, Brazil"
    result = geocoder.geocode(query)
    return (result[0]['geometry']['lat'], result[0]['geometry']['lng']) if result else (None, None)