from bs4 import BeautifulSoup
import pandas as pd
import glob

equipo_diccionario = {
    "529": "FC Barcelona",
    "530": "Atlético de Madrid",
    "531": "Athletic Club",
    "532": "Valencia CF",
    "533": "Villarreal CF",
    "534": "Las Palmas",
    "537": "Leganés",
    "538": "Celta de Vigo",
    "540": "Espanyol",
    "541": "Real Madrid",
    "542": "Alavés",
    "543": "Real Betis",
    "546": "Espanyol",
    "547": "Girona",
    "548": "Real Sociedad",
    "720": "Valladolid",
    "727": "Osasuna",
    "728": "Rayo Vallecano",
    "798": "Mallorca"
}

archivos_html = glob.glob("./estadisticas_fantasy*.html")

data = []

for i in range(1,13):
    archivo = filename = f"./estadisticas{i}.html"
    with open(archivo, encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    tabla = soup.find("table", {"class": "custom-table"})

    if tabla:
        filas = tabla.find_all("tr")
        for fila in filas[1:]:  # Ignorem encapçalament
            columnas = fila.find_all("td")
            nombre_columna = columnas[1]
            nombre_completo = nombre_columna.text.strip()

            imagenes = nombre_columna.find_all("img")
            if len(imagenes) > 1:
                escudo_url = imagenes[1].get("src")
                escudo_id = escudo_url.split("/")[-1].split(".")[0]  # ID de l'escut
                equipo_nombre = equipo_diccionario.get(escudo_id, "Equipo desconocido")
            else:
                escudo_url = None
                equipo_nombre = "Equipo desconocido"

            fila_datos = {
                "Nombre": nombre_completo[2:].strip(),  # Resta de lletres son nom
                "Posición": nombre_completo[:2].strip(),  # Dos primeres lletres son posicio
                "Equipo": equipo_nombre,
                "Puntos": columnas[2].text.strip(),
                "Media Puntos Relevo": columnas[3].text.strip(),
                "Puntos Relevo": columnas[4].text.strip(),
                "Precio": columnas[5].text.strip(),
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
                "Goles en Propia Puerta": columnas[27].text.strip()
            }

            data.append(fila_datos)

df = pd.DataFrame(data)
print(df)

df.to_csv("estadisticas_fantasy.csv", index=True, encoding='utf-8')
