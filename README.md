# Programación Orientada a Objetos - UNAL

## Clase 15: Generadores - Decoradores

## Generadores

Los generadores son una función especial en Python que permiten iterar de forma eficiente y perezosa. En lugar de devolver todos los valores de una vez (como con return), los generadores producen valores uno a uno bajo demanda mediante la palabra clave yield. Cada vez que se invoca al generador, este devuelve un valor y pausa su ejecución, reanudándola en el siguiente yield.

```python 
def contador(n):
  while n > 0:
    yield n
    n -= 1

for num in contador(5):
  print(num)
```

### `yield`

La palabra clave yield convierte una función en un generador. A diferencia de return, no termina la ejecución de la función, sino que la suspende, recordando el estado para continuar posteriormente.

```python 
def generador_simple():
  yield 1
  yield 2
  yield 3

gen = generador_simple()
print(next(gen))  
print(next(gen))  
print(next(gen))  
```

### Conexión con iteradores
Un generador en Python es un tipo de iterador que implementa los métodos __iter__() y __next__() de forma automática al utilizar yield. Cada vez que se llama a next(), la ejecución continúa hasta encontrar el siguiente yield.

 ```mermaid
classDiagram
  class Generador {
    +__iter__()
    +__next__()
  }
  class FuncionesGeneradoras {
    +yield()
  }

  Generador --|> FuncionesGeneradoras
```

### Diferencias con funciones
| Característica  | Funciones  | Generadores  |
|---|---|---|
| **Retornar valores** | Devuelven todos los valores de una vez. | Producen los valores uno por uno |
| **Memoria**  | Necesitan mucho espacio en memoria si los datos son grandes. | Ahorra memoria porque no se almacena toda la secuencia |
| **Eficiencia**  | Tienen una ejecución más rápida en casos simples, pero son ineficientes para datos muy grandes o infinitos. | Son ideales para flujos de datos continuos o secuencias infinitas |

## Casos de uso

1. Secuencias Infinitas: Los generadores son ideales para crear secuencias infinitas sin consumir excesiva memoria. Un ejemplo es la generación de números naturales.

```python 
def numeros_naturales():
  n = 0
  while True:
    yield n
    n += 1

# Uso del generador
gen = numeros_naturales()
for i in range(10):
  print(next(gen))
```

2. Secuencias personalizadas: Los generadores pueden crear secuencias personalizadas, como la secuencia de Fibonacci, que crece exponencialmente.

```python 
def fibonacci():
  a, b = 0, 1
  while True:
    yield a
    a, b = b, a + b

# Ejemplo de uso
gen = fibonacci()
for _ in range(10):
  print(next(gen))
```

3. Manejo de Grandes Volúmenes de Datos: Cuando se manejan archivos o flujos de datos grandes, cargar todo en memoria puede ser ineficiente. Los generadores permiten procesar línea por línea.

```python 
def leer_archivo_grande(ruta):
  with open(ruta) as archivo:
    for linea in archivo:
      yield linea

# Ejemplo de uso
for linea in leer_archivo_grande('mbox.txt'):
  print(linea.strip())
```

4. Generación de datos sinteticos: Los generadores pueden ser útiles para generar grandes cantidades de datos sintéticos, como datos de usuario.

```python 
import random

def generar_datos_usuarios(num_usuarios):
  nombres = ['Juan', 'Ana', 'Alicia', 'Roberto']
  apellidos = ['Pérez', 'García', 'Rodríguez', 'López']
  for _ in range(num_usuarios):
    yield {
      'nombre': random.choice(nombres),
      'apellido': random.choice(apellidos),
      'edad': random.randint(18, 70)
    }

# Generar y mostrar datos de 100 usuarios
for usuario in generar_datos_usuarios(100):
  print(usuario)
```

**Fuentes:**
 + [Understanding Generators in Python with Code Examples](https://medium.com/@siladityaghosh/understanding-generators-in-python-with-code-examples-9a139fc196b6)
 + [Understanding Python Generators: For Complete Beginners](https://medium.com/@abdulrehmanrizwan81/understanding-python-generators-for-complete-beginners-6a6973887a29)
 + [Python Generators — .send() And “x = yield” Explained in 240 Seconds](https://levelup.gitconnected.com/python-generators-send-and-x-yield-explained-in-240-seconds-6d71985b3381)
 + Python 3 Object Oriented Programming - Chap 9.


## Decoradores

### Closures



