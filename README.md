# Programación Orientada a Objetos - UNAL

## Clase 15: Generadores - Decoradores

## Generadores

Los generadores son una función especial en Python que permiten iterar de forma eficiente y *perezosa*. En lugar de devolver todos los valores de una vez (como con `return`), los generadores producen valores uno a uno bajo demanda mediante la palabra clave `yield`. Cada vez que se invoca al generador, este devuelve un valor y pausa su ejecución, reanudándola en el siguiente `yield`.

```python 
def contador(n):
  while n > 0:
    yield n
    n -= 1

for num in contador(5):
  print(num)
```

```python
def contador(n):
  while n > 0:
    yield n
    n -= 1

contador_gen = contador(5)
print(next(contador_gen))
print(next(contador_gen))
```

### `yield`

La palabra clave `yield` convierte una función en un generador. A diferencia de `return`, no termina la ejecución de la función, sino que la suspende, recordando el estado para continuar posteriormente.

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
Un generador en Python es un tipo de iterador que implementa los métodos `__iter__` y `__next__` de forma automática al utilizar `yield`. Cada vez que se llama a `next()`, la ejecución continúa hasta encontrar el siguiente `yield`.

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
| **Retornar valores** | Devuelven todos los valores de una vez | Producen los valores uno por uno |
| **Memoria**  | Necesitan mucho espacio en memoria si los datos son grandes | Ahorra memoria porque no se almacena todos los datos, sino que se van *generando* |
| **Eficiencia**  | Tienen una ejecución más rápida en casos simples, pero son ineficientes para datos muy grandes o infinitos | Son ideales para flujos de datos continuos o secuencias infinitas |

## Casos de uso

1. Secuencias Infinitas: Los generadores son ideales para crear secuencias infinitas sin consumir demasiado espacio en memoria. 

```python 
# Geneacion de todos los nuemros naturales
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

2. Secuencias personalizadas: Los generadores pueden crear secuencias personalizadas, como la secuencia de Fibonacci.

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

3. Manejo de grandes volúmenes de datos: Cuando se manejan archivos o flujos de datos grandes, cargar todo en memoria puede ser ineficiente. Los generadores permiten procesar línea por línea.

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

```python
# Ejemplo completo
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
```

**Fuentes:**
 + [Understanding Generators in Python with Code Examples](https://medium.com/@siladityaghosh/understanding-generators-in-python-with-code-examples-9a139fc196b6)
 + [Understanding Python Generators: For Complete Beginners](https://medium.com/@abdulrehmanrizwan81/understanding-python-generators-for-complete-beginners-6a6973887a29)
 + [Python Generators — .send() And “x = yield” Explained in 240 Seconds](https://levelup.gitconnected.com/python-generators-send-and-x-yield-explained-in-240-seconds-6d71985b3381)
 + Python 3 Object Oriented Programming - Chap 9.


## Decoradores

Los decoradores en Python son una herramienta poderosa para modificar o extender la funcionalidad de métodos sin alterar su código original. 

Implementan el patrón de diseño decorador, que permite añadir comportamiento adicional a objetos de manera dinámica.

### Closures
Un *closure* es una técnica que permite que una función recuerde el entorno en el que fue creada, incluso después de que la función externa haya terminado su ejecución. Los decoradores en Python se basan en *closures* para mantener el estado de una función externa dentro de una función "encerrada" (de ahí viene el nombre closure).

```python 
def outer_func(msg):
  message = msg
  def inner_func():
    print(message)
  return inner_func

# inner_func_with_mem es objeto funcion, ya que outer_func retorna a inner_func
inner_func_with_mem = outer_func("Soy un mensaje")
# Invocacion real de la funcion que en memoria almacenó lo que se envió como argumento msg
inner_func_with_mem()
```

```python 
def outer_func(msg):
  message = msg
  def inner_func(from_msg, to_msg):
    print(f"""
    From: {from_msg}
    To: {to_msg}

    {message}
    """)
  return inner_func

# inner_func_with_mem es objeto funcion, ya que outer_func retorna a inner_func
inner_func_with_mem = outer_func("Cordial saludo...yada yada")
# Invocacion real de la funcion que en memoria almacenó lo que se envió como argumento msg, y tambien puede recibir argumentos
inner_func_with_mem("mi yo del futuro", "mi yo del pasado")
```

```python 
def outer_func(func):
  def wrapped_inner_func(*args):
    func(args[0], args[1])
    print(args[2])
  return wrapped_inner_func

def inner_func(from_msg, to_msg):
    print(f"""
    From: {from_msg}
    To: {to_msg}
    """)

# inner_func_wrapped es objeto funcion que recibió a inner_func como argumento, y outer_func retorna a inner_func con una funcionalidad adicional 
inner_func_wrapped = outer_func(inner_func)
# inner_func_wrapped es invocada, permite tener argmentos adicionales a inner_func sin haber modificado su definicion -- extensibilidad --
inner_func_wrapped("mi yo del futuro", "mi yo del pasado", "Cordial saludo...yada yada")
```

### Funciones revisted (como por cuarta vez)
En Python, las funciones pueden ser pasadas como argumentos a otras funciones y también retornar una función como resultado, a esto se le denomina *funciones de orden superior*. Esto es fundamental para los decoradores, ya que toman una función como argumento y devuelven una nueva función que envuelve (*wrapped*) la original.

```python 
# concepto basico de closure
def create_adder(base_number):
  print("Before returning the function")
  # base_number quedara guardado en memoria si se almacena como variable, create_adder, la cual al ser invocada ejecutara la operación definida en adder
  def adder(number):
    # Acciones que se pueden realizar antres de la logica de la función
    return base_number + number
  print("After returning the function")
  return adder

add_five = create_adder(5)
print(add_five(3)) 
```

```python 
def wrapper(func):
  def inner(*args, **kwargs):
    print("Before calling function")
    result = func(*args, **kwargs)
    print(result)
    print("After calling function")
    return result
  return inner

def add(a, b):
  return a + b

add_wrapper = wrapper(add)
print(add(3, 5))
print("-"*20)
print(add_wrapper(3, 5))
```

```python 
def wrapper(func):
  def inner(*args, **kwargs):
    print(f"args: {args} ::: kwargs {kwargs}")
    print("Before calling function")
    result = func(*args, **kwargs)
    print("After calling function")
    return result
  return inner

@wrapper
def add(a, b):
  return a + b

print(add(3, 5))
print(add(a=3, b=5))
```


### Definción (formal)
Un decorador es una función que toma otra función y le añade algún comportamiento o funcionalidad. El decorador devuelve una nueva función que envuelve a la original.

**Ejemplo:** Decorador de Temporización:

```python 
import time

def timing_decorator(func):
  def wrapper(*args, **kwargs):
    start_time = time.time()
    # ejecucion de la funcion que recibe como argumento
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.4f} seconds")
    return result
  # retorna la funcion decorada sin ejecutarla
  return wrapper

@timing_decorator
def slow_function(seconds):
  time.sleep(seconds)
  return "Done"

print(slow_function(2))
```

### Uso del `@`
El símbolo @ se utiliza en Python para aplicar decoradores de manera más legible y directa. Esto es un atajo que hace que el código sea más claro y conciso.

```python 
@timing_decorator
def example_function():
  pass

# el equivalente seria
#timing_func = timing_decorator(example_function)
#timing_func(*args)
```

### Casos de Uso 

1. Validación de Entradas de Usuario: Los decoradores pueden ser usados para validar entradas antes de que una función procese los datos.

```python 
def validate_inputs(func):
  def wrapper(*args, **kwargs):
    if not all(isinstance(arg, int) for arg in args):
      raise ValueError("All arguments must be integers")
    return func(*args, **kwargs)
  return wrapper

@validate_inputs
def add_numbers(a, b):
  return a + b

print(add_numbers(1, 2))
```

2. Registro de Actividades: Los decoradores son útiles para registrar información sobre la ejecución de funciones --logger--.

```python 
def log_activity(func):
  def wrapper(*args, **kwargs):
    print(f"Executing {func.__name__} with arguments: {args}, {kwargs}")
    return func(*args, **kwargs)
  return wrapper

@log_activity
def process_data(data):
  return data.lower()

print(process_data("sAmplE tExt"))
```

### Decoradores Comunes en Python

+ `@staticmethod`: Define un método que no recibe una referencia a la instancia (self). Por lo tanto se puede usar sin que este asociado a una instancia de la clase, invocandolo con el operador `.`.

```python 
class MyClass:
  @staticmethod
  def static_method():
    return "Static method called"

print(MyClass.static_method())
```

+ `@classmethod`: Define un método que recibe una referencia a la clase (cls) en lugar de una instanci1a, por ende pueden acceder a los atributos de la clase (y en consecuencia a todas sus instancias).

```python 
class MyClass:
  class_variable = "Class Variable"

  @classmethod
  def class_method(cls):
    return f"Class method called. Class variable: {cls.class_variable}"

print(MyClass.class_method())


```

+ `@property`: Define un método que puede ser accedido como un atributo. Esto es particularmente util cuando se aplica encapsulamiento, en el caso de getters.

```python 
class MyClass:
  def __init__(self):
    self._protected_data = "protegido"

  def get_protected_data(self):
    return self_protected_data

my_object = MyClass()
print(my_object.get_protected_data())
```

```python 
class MyClass:
  def __init__(self):
    self._protected_data = "protegido"

  @property
  def protected_data(self):
    return self._protected_data

my_object = MyClass()
print(my_object.protected_data)
```

**Importante:** Revisar cómo se pueden hacer los setters con decoradores.


+ `@functools.lru_cache`: Guarda en Cache los resultados de una función para reducir los llamados, almacenando resultados previos.

```python 
from functools import lru_cache

@lru_cache(maxsize=None)
def expensive_function(x):
  return x ** 2
```

**Más información:**
+ [Closures by corey Schafer](https://www.youtube.com/watch?v=swU3c34d2NQ&t=611s&ab_channel=CoreySchafer)
 + [Decoradores by Corey Schafer](https://www.youtube.com/watch?v=bD05uGo_sVI&ab_channel=CoreySchafer)
 + [Python Decorators That Can Reduce Your Code By Half](https://medium.com/@ayush-thakur02/python-decorators-that-can-reduce-your-code-by-half-b19f673bc7d8)
 + [Mastering Python Decorators: A Comprehensive Guide for Enhancing Code Modularity and Functionality](https://medium.com/@ewho.ruth2014/mastering-python-decorators-a-comprehensive-guide-for-enhancing-code-modularity-and-818ae455260d)
 + [https://levelup.gitconnected.com/how-works-in-python-1f3ca1aac731](https://levelup.gitconnected.com/how-works-in-python-1f3ca1aac731)
 + [8 Python Decorator Things I Regret Not Knowing Earlier](https://levelup.gitconnected.com/8-python-decorator-things-i-regret-not-knowing-earlier-6e886619d75c)
 + Python 3 Object Oriented Programming - Chap 10.

## Reto 7
Our very last challenge (maybe).

1. Add the @property decorator into the package Shape, so all the protected data could be accessed this way.
2. Add @classmethod decorator to Shape, in order to change define and change the type of shape of each class.
3. Add a custom decorator in Shape co show the computation time of at least one operation. e.g: compute_area.