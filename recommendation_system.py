"""Sistema de recomendacion de peliculas basado en su contenido."""

# pandas permite guardar y manipular el catalogo como una tabla.
import pandas as pd

# TfidfVectorizer convierte texto en vectores numericos y cosine_similarity
# mide que tan parecidos son esos vectores.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Catalogo de ejemplo. En una aplicacion real, estos datos podrian cargarse
# desde un archivo CSV o una base de datos.
peliculas = pd.DataFrame(
    [
        {
            "titulo": "Viaje a las estrellas",
            "categoria": "ciencia ficcion aventura",
            "descripcion": "Una tripulacion explora planetas y descubre vida extraterrestre.",
        },
        {
            "titulo": "El planeta perdido",
            "categoria": "ciencia ficcion aventura",
            "descripcion": "Un grupo de astronautas sobrevive en un planeta desconocido.",
        },
        {
            "titulo": "Misterio en la mansion",
            "categoria": "misterio suspenso",
            "descripcion": "Una detective investiga un crimen ocurrido en una casa antigua.",
        },
        {
            "titulo": "La ultima pista",
            "categoria": "misterio suspenso",
            "descripcion": "Un investigador sigue pistas para resolver una desaparicion.",
        },
        {
            "titulo": "Risas de verano",
            "categoria": "comedia romance",
            "descripcion": "Dos amigos viven situaciones divertidas durante sus vacaciones.",
        },
        {
            "titulo": "Un amor inesperado",
            "categoria": "comedia romance",
            "descripcion": "Una pareja se conoce por casualidad y comparte momentos divertidos.",
        },
        {
            "titulo": "Guardianes del bosque",
            "categoria": "animacion aventura",
            "descripcion": "Unos animales trabajan juntos para proteger su hogar natural.",
        },
        {
            "titulo": "La isla secreta",
            "categoria": "aventura misterio",
            "descripcion": "Un equipo busca un tesoro escondido en una isla remota.",
        },
    ]
)

# Se combinan las caracteristicas textuales de cada pelicula en un solo texto.
textos = peliculas["categoria"] + " " + peliculas["descripcion"]

# TF-IDF da mas peso a las palabras utiles para distinguir una pelicula y
# reduce el peso de las palabras que aparecen con frecuencia en todo el catalogo.
vectorizador = TfidfVectorizer()
matriz_tfidf = vectorizador.fit_transform(textos)

# Cada fila de esta matriz contiene la similitud entre una pelicula y todas
# las demas; un valor mas cercano a 1 indica mayor similitud.
matriz_similitud = cosine_similarity(matriz_tfidf)


def recomendar(titulo: str, cantidad: int = 3) -> pd.DataFrame:
    """Devuelve las peliculas mas similares al titulo indicado."""
    # Se comprueba la entrada para dar un error claro si el titulo no existe.
    coincidencias = peliculas.index[peliculas["titulo"] == titulo]
    if coincidencias.empty:
        raise ValueError(f"No se encontro la pelicula: {titulo}")
    if cantidad < 0:
        raise ValueError("La cantidad de recomendaciones no puede ser negativa.")

    # Se obtiene la posicion de la pelicula y sus similitudes con el catalogo.
    indice = coincidencias[0]
    puntuaciones = list(enumerate(matriz_similitud[indice]))

    # Se ordena de mayor a menor y se excluye la pelicula consultada.
    puntuaciones.sort(key=lambda elemento: elemento[1], reverse=True)
    mejores = [
        (otro_indice, puntuacion)
        for otro_indice, puntuacion in puntuaciones
        if otro_indice != indice
    ][:cantidad]

    # Se prepara una tabla facil de leer con las recomendaciones y su puntuacion.
    indices = [otro_indice for otro_indice, _ in mejores]
    resultado = peliculas.iloc[indices][["titulo", "categoria"]].copy()
    resultado["similitud"] = [puntuacion for _, puntuacion in mejores]
    return resultado.reset_index(drop=True)


# Esta demostracion se ejecuta solo al lanzar este archivo directamente,
# no cuando se importa desde otro modulo.
if __name__ == "__main__":
    pelicula_elegida = "Viaje a las estrellas"
    print(f"Recomendaciones para «{pelicula_elegida}»:")
    print(recomendar(pelicula_elegida).to_string(index=False))