import pygame
import os
import json
from parametros import *
from biblioteca import *
from datos import lista

# Cambiar el directorio de trabajo al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Inicialización de variables
pregunta_actual = ""
opcion_a = ""
opcion_b = ""
opcion_c = ""
lista_preguntas = []
lista_opciones_a = []
lista_opciones_b = []
lista_opciones_c = []
lista_correctas = []
jugadores = []
indice_pregunta = 0

for pregunta in lista:
    lista_preguntas.append(pregunta["pregunta"])
    lista_opciones_a.append(pregunta["a"])
    lista_opciones_b.append(pregunta["b"])
    lista_opciones_c.append(pregunta["c"])
    lista_correctas.append(pregunta["correcta"])

# Inicializamos el juego
pygame.init()

# Crear la pantalla 
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
# Título de la ventana
pygame.display.set_caption("Carrera UTN")

# Cargar imágenes
imagen_logo, imagen_utn, imagen_flecha, imagen_flecha_2, imagen_personaje = cargar_imagenes()

# Rectángulos del personaje y casillas
rect_personaje = imagen_personaje.get_rect()
rect_personaje.x = 664
rect_personaje.y = 120
# Rectángulos de las casillas superiores
rect_casilla_inicio = pygame.Rect(90, 300, 80, 50)
rect_casilla_1 = pygame.Rect(190, 300, 80, 50)
rect_casilla_2 = pygame.Rect(280, 300, 80, 50)
rect_casilla_3 = pygame.Rect(370, 300, 80, 50)
rect_casilla_4 = pygame.Rect(460, 300, 80, 50)
rect_casilla_5 = pygame.Rect(550, 300, 80, 50)
rect_casilla_avanzar = pygame.Rect(640, 300, 80, 50)
rect_casilla_7 = pygame.Rect(730, 300, 80, 50)
rect_casilla_8 = pygame.Rect(820, 300, 80, 50)
# Rectángulos de las casillas inferiores
rect_casilla_9 = pygame.Rect(820, 450, 80, 50)
rect_casilla_10 = pygame.Rect(730, 450, 80, 50)
rect_casilla_11 = pygame.Rect(640, 450, 80, 50)
rect_casilla_12 = pygame.Rect(550, 450, 80, 50)
rect_casilla_retroceder = pygame.Rect(460, 450, 80, 50)
rect_casilla_14 = pygame.Rect(370, 450, 80, 50)
rect_casilla_15 = pygame.Rect(280, 450, 80, 50)
rect_casilla_16 = pygame.Rect(190, 450, 80, 50)
rect_casilla_final = pygame.Rect(20, 450, 80, 50)
# Lista de casillas
casillas = [
    rect_casilla_inicio, rect_casilla_1, rect_casilla_2, rect_casilla_3, rect_casilla_4,
    rect_casilla_5, rect_casilla_avanzar, rect_casilla_7, rect_casilla_8,
    rect_casilla_9, rect_casilla_10, rect_casilla_11, rect_casilla_12,
    rect_casilla_retroceder, rect_casilla_14, rect_casilla_15, rect_casilla_16, rect_casilla_final
]
# Rectángulos de los botones comenzar y terminar
rect_comenzar = pygame.Rect(225, 550, 200, 100)
rect_terminar = pygame.Rect(575, 550, 200, 100)
# Rectángulos de las respuestas
rect_opcion_a = pygame.Rect(310, 100, 300, 20)
rect_opcion_b = pygame.Rect(310, 140, 300, 20)
rect_opcion_c = pygame.Rect(310, 180, 300, 20)

# Parte de escribir y guardar el nombre
nombre_jugador = ""
rect_nombre = pygame.Rect(850, 500, 200, 25)
rect_nombre_escrito = pygame.Rect(850, 500, 200, 25)
rect_listo = pygame.Rect(850, 550, 65, 30)

# Fuentes
fuente_grande = pygame.font.SysFont("Arial", 45)
fuente_mediana = pygame.font.SysFont("Calibri", 25)
fuente_pequena = pygame.font.SysFont("Arial", 18)
# Textos juego
txt_tiempo = fuente_grande.render("Tiempo:", True, COLOR_LETRAS_GRIS)
txt_puntaje = fuente_grande.render("Puntaje:", True, COLOR_LETRAS_GRIS)
txt_avanza = fuente_pequena.render("Avanza", True, COLOR_NEGRO)
txt_retrocede = fuente_pequena.render("Retrocede", True, COLOR_NEGRO)
txt_1 = fuente_pequena.render("1", True, COLOR_NEGRO)
txt_salida = fuente_mediana.render("Inicio", True, COLOR_NEGRO)
txt_llegada = fuente_mediana.render("Final", True, COLOR_NEGRO)
txt_comenzar = fuente_grande.render("Comenzar", True, COLOR_LETRAS_GRIS_OSCURO)
txt_terminar = fuente_grande.render("Terminar", True, COLOR_LETRAS_GRIS_OSCURO)
# Texto juego terminado
txt_puntaje_tabla = fuente_grande.render("Puntajes", True, COLOR_LETRAS_GRIS)

# Timer 1 segundo
timer_segundos = pygame.USEREVENT
pygame.time.set_timer(timer_segundos, 1000) # 1000 es 1 segundo
segundos_restantes = 5
flag_tiempo = False

# Puntaje
puntaje_actual = 0
indice_casilla = 0

flag_nombre = False
flag_guardar_datos = False

flag_acc_avanzar = False
flag_acc_retroceder = False
flag_correcta = False
flag_incorrecta = False
flag_comenzar = False
flag_terminar = False 
flag_posicionar_personaje = False 
flag_juego_corriendo = True

# Nombre del archivo JSON
archivo_json = 'datos.json'

# Verificar si el archivo JSON existe
if os.path.exists(archivo_json):
    # Cargar datos existentes si el archivo ya existe
    with open(archivo_json, 'r') as archivo:
        jugadores = json.load(archivo)

while flag_juego_corriendo:
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        # Si el evento es salir, cierra la ventana
        if evento.type == pygame.QUIT:
            flag_juego_corriendo = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            posicion_click = list(evento.pos)
            if rect_comenzar.collidepoint(evento.pos):
                flag_comenzar = True
                flag_posicionar_personaje = True
            if rect_terminar.collidepoint(evento.pos):
                flag_terminar = True

            if rect_opcion_a.collidepoint(evento.pos):
                if lista_correctas[indice_pregunta] == "a":
                    flag_correcta = True
                else:
                    flag_incorrecta = True
            elif rect_opcion_b.collidepoint(evento.pos):
                if lista_correctas[indice_pregunta] == "b":
                    flag_correcta = True
                else:
                    flag_incorrecta = True
            elif rect_opcion_c.collidepoint(evento.pos):
                if lista_correctas[indice_pregunta] == "c":
                    flag_correcta = True
                else:
                    flag_incorrecta = True

            if rect_nombre.collidepoint(evento.pos):
                flag_nombre = True
            else:
                flag_nombre = False
            
            if rect_listo.collidepoint(evento.pos):
                flag_guardar_datos = True

        if evento.type == pygame.KEYDOWN and flag_nombre:
            if evento.key == pygame.K_BACKSPACE:
                nombre_jugador = nombre_jugador[0:-1]
            else:
                nombre_jugador += evento.unicode
        
        if evento.type == pygame.USEREVENT:
            if evento.type == timer_segundos:
                if flag_tiempo == False:
                    segundos_restantes = int(segundos_restantes) - 1
                    if int(segundos_restantes) == -1:
                        flag_tiempo = True
                        segundos_restantes = "Fin"

    # Pintar el fondo de la pantalla 
    pantalla.fill(COLOR_PANTALLA)

    if not flag_terminar:
        # Imagen de logo
        pantalla.blit(imagen_logo, (20, 20))
        pantalla.blit(imagen_utn, (20, 450))
        pantalla.blit(imagen_flecha, (90, 300))
        pantalla.blit(imagen_flecha_2, (930, 325))

        # Dibujamos rectángulos
        pygame.draw.rect(pantalla, COLOR_RECT_VERDE, (270, 20, 560, 200))

        # Rectángulos del camino superior
        pygame.draw.rect(pantalla, COLOR_NARANJA, rect_casilla_1, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_VERDE_AGUA, rect_casilla_2, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_AMARILLO, rect_casilla_3, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_CELESTE, rect_casilla_4, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_ROJO, rect_casilla_5, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_VIOLETA, rect_casilla_avanzar, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_BEIGE, rect_casilla_7, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_VERDE, rect_casilla_8, border_radius=10)
        # Rectángulos del camino inferior
        pygame.draw.rect(pantalla, COLOR_VERDE, rect_casilla_9, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_BEIGE, rect_casilla_10, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_VIOLETA, rect_casilla_11, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_ROJO, rect_casilla_12, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_CELESTE, rect_casilla_retroceder, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_AMARILLO, rect_casilla_14, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_VERDE_AGUA, rect_casilla_15, border_radius=10)
        pygame.draw.rect(pantalla, COLOR_NARANJA, rect_casilla_16, border_radius=10)
        # Rectángulos de comenzar y terminar. 
        pygame.draw.rect(pantalla, COLOR_BOTONES, rect_comenzar, border_radius=25)
        pygame.draw.rect(pantalla, COLOR_BOTONES, rect_terminar, border_radius=25)
        # Prueba de rectángulo para respuesta
        pygame.draw.rect(pantalla, COLOR_RECT_VERDE, rect_opcion_a, width=3)
        pygame.draw.rect(pantalla, COLOR_RECT_VERDE, rect_opcion_b, width=3)
        pygame.draw.rect(pantalla, COLOR_RECT_VERDE, rect_opcion_c, width=3)

        # Texto de tiempo y puntaje
        pantalla.blit(txt_tiempo, (850, 20)) 
        pantalla.blit(txt_puntaje, (850, 130)) 
        # Texto de retroceder y avanzar
        pantalla.blit(txt_avanza, (655, 309)) 
        pantalla.blit(txt_1, (676, 329)) 
        pantalla.blit(txt_retrocede, (463, 459)) 
        pantalla.blit(txt_1, (493, 480))  
        # Textos de salida y llegada
        pantalla.blit(txt_salida, (20, 315)) 
        # Textos de comenzar y terminar
        pantalla.blit(txt_comenzar, (240, 580))
        pantalla.blit(txt_terminar, (590, 580))
        # Texto timer
        
        if flag_comenzar: 
            txt_timer = fuente_grande.render(str(segundos_restantes), True, COLOR_LETRAS_GRIS)
            pantalla.blit(txt_timer, (1025, 20))
            pregunta_actual = lista_preguntas[indice_pregunta]
            opcion_a = lista_opciones_a[indice_pregunta]
            opcion_b = lista_opciones_b[indice_pregunta]
            opcion_c = lista_opciones_c[indice_pregunta]

            # Texto pregunta
            txt_pregunta = fuente_pequena.render(str(pregunta_actual), True, COLOR_NEGRO)
            pantalla.blit(txt_pregunta, (310, 50))
            txt_res_a = fuente_pequena.render(str(opcion_a), True, COLOR_NEGRO)
            pantalla.blit(txt_res_a, (310, 100))
            txt_res_b = fuente_pequena.render(str(opcion_b), True, COLOR_NEGRO)
            pantalla.blit(txt_res_b, (310, 140))
            txt_res_c = fuente_pequena.render(str(opcion_c), True, COLOR_NEGRO)
            pantalla.blit(txt_res_c, (310, 180))

            if flag_posicionar_personaje:
                rect_personaje.centerx = casillas[0].centerx
                rect_personaje.centery = casillas[0].centery
                flag_posicionar_personaje = False
        
        if flag_correcta:
            puntaje_actual += 10
            indice_casilla += 2
            if indice_casilla >= (len(casillas) - 1):
                rect_personaje.centerx = casillas[-1].centerx
                rect_personaje.centery = casillas[-1].centery
                flag_terminar = True
            else:
                rect_personaje.centerx = casillas[indice_casilla].centerx
                rect_personaje.centery = casillas[indice_casilla].centery
        txt_puntaje_num = fuente_grande.render(str(puntaje_actual), True, COLOR_LETRAS_GRIS)
        pantalla.blit(txt_puntaje_num, (1025, 130))

        if flag_incorrecta:
            if indice_casilla <= 0:
                rect_personaje.centerx = casillas[0].centerx
                rect_personaje.centery = casillas[0].centery
            else:
                indice_casilla -= 1
                rect_personaje.centerx = casillas[indice_casilla].centerx
                rect_personaje.centery = casillas[indice_casilla].centery

            # Pasar a la siguiente pregunta inmediatamente
            indice_pregunta += 1
            if indice_pregunta >= len(lista_preguntas):
                indice_pregunta = 0
            pregunta_actual = lista_preguntas[indice_pregunta]
            opcion_a = lista_opciones_a[indice_pregunta]
            opcion_b = lista_opciones_b[indice_pregunta]
            opcion_c = lista_opciones_c[indice_pregunta]
            segundos_restantes = 5
            flag_incorrecta = False

        if rect_personaje.colliderect(rect_casilla_avanzar):
            flag_acc_avanzar = True
        if rect_personaje.colliderect(rect_casilla_retroceder):
            flag_acc_retroceder = True  

        if flag_acc_avanzar:
            indice_casilla += 1
            rect_personaje.centerx = casillas[indice_casilla].centerx
            rect_personaje.centery = casillas[indice_casilla].centery
            flag_acc_avanzar = False

        if flag_acc_retroceder:
            if flag_correcta:
                indice_casilla -= 2
            else:
                indice_casilla -= 1
            rect_personaje.centerx = casillas[indice_casilla].centerx
            rect_personaje.centery = casillas[indice_casilla].centery
            flag_acc_retroceder = False

        if flag_tiempo or flag_correcta or flag_incorrecta:
            indice_pregunta += 1 
            if indice_pregunta >= len(lista_preguntas):
                indice_pregunta = 0
            segundos_restantes = 5
            flag_tiempo = False
            flag_correcta = False
            flag_incorrecta = False

        # Imprimir en pantalla los Rect()
        pantalla.blit(imagen_personaje, rect_personaje)

    else:
        pantalla.blit(imagen_logo, (20, 20))
        pantalla.blit(txt_puntaje_tabla, (430, 50)) 
        # Personaje
        imagen_personaje = pygame.transform.scale(imagen_personaje, (100, 200))
        rect_personaje.x = 50
        rect_personaje.y = 350      
        pantalla.blit(imagen_personaje, rect_personaje)

        # Renderizar nombres y puntajes
        y_offset = 150
        jugadores_ordenados = ordenamiento(jugadores, "puntaje", True)[:10]
        for jugador in jugadores_ordenados:
            nombre_render = fuente_grande.render(jugador['nombre'], True, COLOR_NEGRO)
            puntaje_render = fuente_grande.render(str(jugador['puntaje']), True, COLOR_NEGRO)
            pantalla.blit(nombre_render, (400, y_offset))
            pantalla.blit(puntaje_render, (660, y_offset))
            y_offset += 50

        # Casilla para el nombre
        pygame.draw.rect(pantalla, COLOR_NEGRO, rect_nombre, width=2)
        txt_nombre_info = fuente_mediana.render("Aca escribi tu nombre", True, COLOR_NEGRO)
        pantalla.blit(txt_nombre_info, (rect_nombre.x, rect_nombre.y - 30))
        nombre_escrito = fuente_mediana.render(nombre_jugador, True, COLOR_NEGRO)
        pygame.draw.rect(pantalla, COLOR_NEGRO, rect_nombre_escrito, width=2)
        pantalla.blit(nombre_escrito, (rect_nombre_escrito.x + 5, rect_nombre_escrito.y + 1)) 

        pygame.draw.rect(pantalla, COLOR_GRIS, rect_listo)
        txt_listo = fuente_mediana.render("Listo", True, COLOR_BLANCO)
        pantalla.blit(txt_listo, (rect_listo.x + 5, rect_listo.y + 5))

        if flag_guardar_datos:
            # Actualizar el puntaje en el archivo JSON
            actualizar_puntajes(nombre_jugador, puntaje_actual, archivo_json)
            
            # Recargar la lista de jugadores actualizada
            with open(archivo_json, 'r') as archivo:
                jugadores = json.load(archivo)

            flag_guardar_datos = False

    pygame.display.flip()

pygame.quit()