from fastapi import FastAPI
from typing import Union
from casas import top_desarrolladores_recomendados
#from casas import userdata
#from casas import UserForGenre
from casas import developer
from casas import developer_reviews_analysis
from typing import List, Dict, Tuple, Sequence, Any, Union, Optional, Callable 
from fastapi.responses import JSONResponse
import pandas as pd


app = FastAPI()

@app.get("/top_desarrolladores/{year}")
async def get_top_desarrolladores(year: int):
    top_desarrolladores = top_desarrolladores_recomendados(year)

    # Devolver el resultado
    return {f"top_desarrolladore 1" : top_desarrolladores[0], "top_desarrollador 2" : top_desarrolladores[1], "top_desarrollador 3" : top_desarrolladores[2]}


'''@app.get("/userdata/{user_id}")
async def get_userdata(user_id: Union[int, str]):
    # Obtener los datos del usuario
    user_data = userdata(user_id)

    # Devolver el resultado
    return user_data'''

'''@app.get("/UserForGenre/{genero}")
async def get_UserForGenre(genero: str):
    # Obtener los datos del usuario
    user_data = UserForGenre(genero)

    # Devolver el resultado
    return user_data'''


@app.get("/developer/{developer_name}")
async def get_developer_data(developer_name: str):
    # Obtener los datos del desarrollador
    developer_data = developer(developer_name)

    # Devolver el resultado como respuesta JSON
    return JSONResponse(developer_data.to_dict(orient="records"))

@app.get("/developer_reviews_analysis/{developer_name}")
async def get_developer_reviews_analysis(developer_name: str):
    # Obtener los datos del desarrollador
    developer_data = developer_reviews_analysis(developer_name)

    # Devolver el resultado como respuesta JSON
    return developer_data