import pandas as pd    # Para manejo de datos
import numpy as np    # Para operaciones matemáticas
import os   # Para manejo de archivos
import datetime as dt   # Para manejo de fechas
import json   # Para manejo de archivos json
import gc   # Para garbage collector


df7 = pd.read_parquet('User_reviews_reducido_32.parquet')
df8 = pd.read_parquet('Output_steam_games_reducido_32.parquet')
#df9 = pd.read_parquet('User_items_reducido_32.parquet')
merged_df = pd.read_parquet('Top 3 Desarrolladores.parquet')
#merged_df5 = pd.read_parquet('User_Data.parquet')
#merged_df10 = pd.merge(df8, df9, on='Item_Id')
#df_nuevo = merged_df10.drop(columns=['Item_Id','App_name','Price','Developer','Items_Count','Item_Name'])
#df_f1 = df8[["Item_Id", "Price","Developer","Release_year"]]
#df_merged123 = pd.merge(df8, df7, on='Item_Id') 
#df_limpio = df_merged123[['User_Id', 'Item_Id','Developer','Release_year','Sentiment Analysis']]


def top_desarrolladores_recomendados(year):
    # Cargar el DataFrame de juegos
    

    # Filtrar los juegos por año
    df_year = merged_df[merged_df['year'] == year]

    # Agrupar los juegos por desarrollador y contar el número de juegos recomendados
    df_count = df_year[df_year['Recommend'] == True][df_year['Sentiment Analysis'] == 2].groupby('Developer')['App_name'].count().reset_index()

    # Ordenar los resultados por número de juegos recomendados y devolver los tres primeros desarrolladores
    top_desarrolladores = df_count.sort_values('App_name', ascending=False).head(3)['Developer'].tolist()
    del df_count, df_year
    gc.collect()
    # Devolver el top 3 de desarrolladores
    return top_desarrolladores

'''def userdata(user_id):
    # Leer los DataFrames necesarios
    merged_df5 = pd.read_parquet('User_data.parquet', columns=['User_Id', 'Price', 'Recommend'])
    df9 = pd.read_parquet('User_items_reducido_32.parquet', columns=['User_Id'])

    if type(user_id) == int:
        user_id = str(user_id)

    if not user_id in merged_df5['User_Id'].values or not user_id in df9['User_Id'].values:
        return f"El user_id {user_id} no existe en la base de datos u.u."

    # Filtrar los DataFrames por user_id
    user_data = merged_df5[merged_df5['User_Id'] == user_id]
    user_items = df9[df9['User_Id'] == user_id]

    # Calcular la cantidad de dinero gastado por el usuario
    dinero_gastado = np.dot(user_data['Price'], user_data['Recommend'])

    # Calcular el porcentaje de recomendación en base a reviews.recommend
    recomendacion = user_data['Recommend'].sum()
    porcentaje_recomendacion = recomendacion / user_data.shape[0] * 100

    # Calcular la cantidad de items
    cantidad_de_items = user_items.shape[0]

    # Crear un diccionario con los resultados
    resultados = {
        'Cantidad de dinero gastado': dinero_gastado,
        'Porcentaje de recomendación': porcentaje_recomendacion,
        'Cantidad de items': cantidad_de_items
    }
    del merged_df5, df9, user_data, user_items
    gc.collect()
    return resultados'''

'''def userdata(user_id):
    
    if type(user_id) == int:
        user_id = str(user_id)

    
    if not user_id in merged_df5['User_Id'].values or not user_id in df9['User_Id'].values:
        return f"El user_id {user_id} no existe en la base de datos u.u."

    user_data = merged_df5[merged_df5['User_Id'] == user_id]

    user_items = df9[df9['User_Id'] == user_id]

    # Calcular la cantidad de dinero gastado por el usuario
    dinero_gastado = user_data['Price'].sum()

    # Calcular el porcentaje de recomendación en base a reviews.recommend
    recomendacion = user_data['Recommend'].sum()
    porcentaje_recomendacion = recomendacion / len(user_data) * 100

    # Calcular la cantidad de items
    cantidad_de_items = user_items['Item_Id'].nunique()

    # Crear un diccionario con los resultados
    resultados = {
        'Cantidad de dinero gastado': dinero_gastado,
        'Porcentaje de recomendación': porcentaje_recomendacion,
        'Cantidad de items': cantidad_de_items
    }
    del user_data, user_items
    gc.collect()
    return resultados'''




'''def UserForGenre(genero):
    if not genero in df_nuevo.columns:
        return f"El género {genero} no existe en la base de datos."
    
    df_genre = df_nuevo[df_nuevo[genero] == 1]

    usur_mas_horas = df_genre.groupby("User_Id")["Playtime_Forever"].sum().idxmax()

    filtro_usur = df_genre[df_genre["User_Id"] == usur_mas_horas]

    horas_jugXaño = filtro_usur.groupby("Release_year")["Playtime_Forever"].sum()

    registro = horas_jugXaño.to_dict()

    Horas_por_año = {}
    for clave, valor in registro.items():
        clave_formateada = f'Año: {int(clave)}'
        valor_formateado = int(valor)
        Horas_por_año[clave_formateada] = valor_formateado
    del df_genre, filtro_usur, horas_jugXaño
    gc.collect()
    return {"Usuario con más horas jugadas": usur_mas_horas, "Horas jugadas por año": Horas_por_año}'''



def developer(developer_name: str):
    # Filtrar los datos del DataFrame por el nombre del desarrollador
    developer_data = df_f1[df_f1["Developer"] == developer_name]

    # Agrupar los datos por año de lanzamiento y contar la cantidad de juegos
    games_per_year = developer_data.groupby("Release_year")["Item_Id"].count()

    # Filtrar los juegos gratuitos del desarrollador y contar la cantidad por año
    free_games = developer_data[developer_data["Price"] == 0]
    free_games_per_year = free_games.groupby("Release_year")["Item_Id"].count()

    # Calcular el porcentaje de juegos gratuitos por año
    free_percentage_per_year = round((free_games_per_year / games_per_year) * 100, 2)

    # Crear una tabla con los resultados
    table = pd.concat([games_per_year, free_percentage_per_year], axis=1)
    table.columns = ["Cantidad de juegos", "Porcentaje de juegos gratuitos"]

    # Eliminar las filas con valores NaN
    table = table.dropna()

    # Agregar el signo de porcentaje a la columna "Porcentaje de juegos gratuitos"
    table["Porcentaje de juegos gratuitos"] = table["Porcentaje de juegos gratuitos"].apply(lambda x: f"{x}%" if not pd.isna(x) else x)

    table = table.reset_index()
    del developer_data, games_per_year, free_games, free_games_per_year, free_percentage_per_year
    gc.collect()
    return table


def developer_reviews_analysis(desarrolladora:str):
    
    # Se filtran las columnas a utilizar y se eliminan duplicados
    df_merged = df_limpio[['User_Id', 'Item_Id','Developer','Release_year','Sentiment Analysis']]


    df_merged = df_merged[df_merged["Developer"] == desarrolladora]

    # Se obtienen la cantidad de reviews positivas y negativas
    positive_reviews = df_merged[df_merged["Sentiment Analysis"] == 2].shape[0]
    negative_reviews = df_merged[df_merged["Sentiment Analysis"] == 0].shape[0]

    # Se crea un string con el resumen de las reviews
    resumen_reviews = f"[Negative = {negative_reviews}, Positive = {positive_reviews}]"

    # Se crea un diccionario con el resumen de las reviews
    dicc = {desarrolladora : resumen_reviews}
    del df_merged, positive_reviews, negative_reviews, resumen_reviews
    gc.collect()
    # Se devuelve un diccionario con los resultados obtenidos
    return dicc