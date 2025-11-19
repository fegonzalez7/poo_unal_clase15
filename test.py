from memory_profiler import memory_usage
import random
import time
from typing import Generator

nombres = ['Juan', 'Ana', 'Alicia', 'Roberto']
carreras = ['Ingeniería', 'Medicina', 'Derecho', 'Arquitectura']

print(f"Memoria inicial: {memory_usage()[0]} MB")


def lista_personas(cant_personas: int) -> list:
    resultado: list = []
    for i in range(cant_personas):
        persona = {
            'id': i,
            'nombre': random.choice(nombres),
            'carrera': random.choice(carreras),
            'edad': random.randint(18, 30)
        }
        resultado.append(persona)
    return resultado

def generador_personas(cant_personas: int) -> Generator[dict, None, None]:
    for i in range(cant_personas):
        persona = {
            'id': i,
            'nombre': random.choice(nombres),
            'carrera': random.choice(carreras),
            'edad': random.randint(18, 30)
        }
        yield persona


tiempo_inicio = time.time()
# personas = generador_personas(1_000_000)
personas = lista_personas(1_000_000)
print(type(personas))
for idx, persona in enumerate(personas):
    if idx % 10000 == 0:
        print(persona)

tiempo_fin = time.time()

print(f"Tiempo de ejecución: {tiempo_fin - tiempo_inicio} segundos")
print(f"Memoria final: {memory_usage()[0]} MB")