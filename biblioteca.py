from copy import deepcopy
import json
from parametros import *
import pygame

def ordenamiento(lista_personajes:list, ordenar_por:str, sentido:bool)-> list:
    copia_lista_personajes = deepcopy(lista_personajes)
    copia_lista_personajes.sort(key = lambda personaje: personaje[ordenar_por], reverse = sentido)
    return copia_lista_personajes

def actualizar_puntajes(nombre, puntaje, archivo='datos.json'):
    """
    Actualiza el puntaje de un jugador en el archivo de datos.
    Si el jugador ya existe y su puntaje es menor, se actualiza con el nuevo puntaje.
    Si el jugador no existe, se añade al archivo.

    Args:
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje del jugador.
        archivo (str): Ruta del archivo de datos JSON. Default es 'datos.json'.
    """
    # Leer los datos existentes
    try:
        with open(archivo, 'r') as file:
            datos = json.load(file)
    except FileNotFoundError:
        datos = []

    # Verificar si el jugador ya existe y actualizar su puntaje si es necesario
    jugador_existente = next((jugador for jugador in datos if jugador['nombre'] == nombre), None)
    if jugador_existente:
        if jugador_existente['puntaje'] < puntaje:
            jugador_existente['puntaje'] = puntaje
    else:
        datos.append({'nombre': nombre, 'puntaje': puntaje})

    # Guardar los datos actualizados
    with open(archivo, 'w') as file:
        json.dump(datos, file, indent=4)

# Función para cargar imágenes
def cargar_imagenes():
    imagen_logo = pygame.image.load("carrera-de-mente.png")
    imagen_logo = pygame.transform.scale(imagen_logo, (230,200))
    imagen_utn = pygame.image.load("logo-utn.png")
    imagen_utn = pygame.transform.scale(imagen_utn, (150,50))
    imagen_flecha = pygame.image.load("flecha.png").convert_alpha()
    imagen_flecha = pygame.transform.scale(imagen_flecha, (90,50))
    imagen_flecha_2 = pygame.image.load("flecha-2.png").convert_alpha()
    imagen_flecha_2 = pygame.transform.scale(imagen_flecha_2, (50,150))
    imagen_personaje = pygame.image.load("personaje.png").convert_alpha()
    imagen_personaje = pygame.transform.scale(imagen_personaje, (50,100))
    return imagen_logo, imagen_utn, imagen_flecha, imagen_flecha_2, imagen_personaje