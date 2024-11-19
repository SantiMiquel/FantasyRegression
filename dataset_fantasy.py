from bs4 import BeautifulSoup
import pandas as pd

equipo_diccionario = {
    "529": "FC Barcelona",
    "530": "Atlético de Madrid",
    "531": "Athletic Club",
    "532": "Valencia CF",
    "533": "Villarreal CF",
    "534": "Las Palmas",
    "536": "Sevilla",
    "537": "Leganés",
    "538": "Celta de Vigo",
    "540": "Espanyol",
    "541": "Real Madrid",
    "542": "Alavés",
    "543": "Real Betis",
    "546": "Getafe",
    "547": "Girona",
    "547_002": "Girona",
    "548": "Real Sociedad",
    "720": "Valladolid",
    "727": "Osasuna",
    "728": "Rayo Vallecano",
    "798": "Mallorca"
}
precios_iniciales = {}
for j in range(1,13):
    archivo_preu = f"../dataset-html/preu_inicial{j}.html"
    with open(archivo_preu, encoding="utf-8") as file_preu:
        html_content_preu = file_preu.read()

    soup_preu = BeautifulSoup(html_content_preu, "html.parser")
    tabla_preu = soup_preu.find("table", {"class": "custom-table"})
    if tabla_preu:
        filas_preu = tabla_preu.find_all("tr")
        for fila_preu in filas_preu[1:]:
            columnas_preu = fila_preu.find_all("td")
            nombre_columna_preu = columnas_preu[1]
            nombre_completo_preu = nombre_columna_preu.text.strip()[2:].strip()       
            precio_inicial = columnas_preu[2].text.strip()
            precios_iniciales[nombre_completo_preu] = precio_inicial



data = []
for i in range(1, 13):
    archivo = f"../dataset-html/estadisticas{i}.html"
    
    with open(archivo, encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    tabla = soup.find("table", {"class": "custom-table"})


    if tabla:
        filas = tabla.find_all("tr")
        for fila in filas[1:]:
            columnas = fila.find_all("td")
            nombre_columna = columnas[1]
            nombre_completo = nombre_columna.text.strip()

            imagenes = nombre_columna.find_all("img")
            if len(imagenes) > 1:
                escudo_url = imagenes[1].get("src")
                escudo_id = escudo_url.split("/")[-1].split(".")[0]
                equipo_nombre = equipo_diccionario.get(escudo_id, "Equipo desconocido")
            else:
                escudo_url = None
                equipo_nombre = "Equipo desconocido"

            fila_datos = {
                "Nombre": nombre_completo[2:].strip(),
                "Posición": nombre_completo[:2].strip(),
                "Equipo": equipo_nombre,
                "Puntos": columnas[2].text.strip(),
                "Media Puntos Relevo": columnas[3].text.strip(),
                "Puntos Relevo": columnas[4].text.strip(),
                "Precio Actual": columnas[5].text.strip()[:-2],
                "Precio Inicial": precios_iniciales.get(nombre_completo[2:].strip())[:-2],
                "Media": columnas[6].text.strip(),
                "Partidos": columnas[7].text.strip(),
                "Minutos": columnas[8].text.strip(),
                "Goles": columnas[9].text.strip(),
                "Asistencias": columnas[10].text.strip(),
                "Asistencias sin Gol": columnas[11].text.strip(),
                "Balones al Área": columnas[12].text.strip(),
                "Despejes": columnas[13].text.strip(),
                "Regates": columnas[14].text.strip(),
                "Tiros a Puerta": columnas[15].text.strip(),
                "Balones Recuperados": columnas[16].text.strip(),
                "Posesiones Perdidas": columnas[17].text.strip(),
                "Penaltis Fallados": columnas[18].text.strip(),
                "Goles en Contra": columnas[19].text.strip(),
                "Tarjetas Rojas": columnas[20].text.strip(),
                "Paradas": columnas[21].text.strip(),
                "Penaltis Cometidos": columnas[22].text.strip(),
                "Tarjetas Amarillas": columnas[23].text.strip(),
                "Segundas Amarillas": columnas[24].text.strip(),
                "Penaltis Provocados": columnas[25].text.strip(),
                "Penaltis Parados": columnas[26].text.strip(),
                "Goles en Propia Puerta": columnas[27].text.strip(),
            }

            data.append(fila_datos)

df = pd.DataFrame(data)

df.to_csv("estadisticas_fantasy.csv", index=True, encoding="utf-8")