<!-- omit from toc -->
# Algoritmo PSO (Particle Swarm Optimization)

Implementación del algoritmo de optimización por enjambre de partículas (PSO) con soporte para diferentes estrategias de peso inercial, funciones de benchmark y graficas de visualización.

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Desinstalación](#desinstalación)
- [Uso sugerido](#uso-sugerido)
  - [Configuración:](#configuración)
  - [Ejecución:](#ejecución)
    - [Individual (Un solo)](#individual-un-solo)
    - [Múltiple](#múltiple)
  - [Parámetros de configuración](#parámetros-de-configuración)
- [Estrategias de Peso Inercial](#estrategias-de-peso-inercial)
  - [1. Valor constante](#1-valor-constante)
  - [2. Estrategias básicas](#2-estrategias-básicas)
  - [3. Estrategias avanzadas](#3-estrategias-avanzadas)
  - [4. Estrategia proopuesta híbrida con coseno](#4-estrategia-proopuesta-híbrida-con-coseno)
  - [5. Estrategias adaptativas](#5-estrategias-adaptativas)
- [Estrategias de Coeficientes](#estrategias-de-coeficientes)
  - [1. Valor constante](#1-valor-constante-1)
  - [2. Estrategias dinámicas](#2-estrategias-dinámicas)
- [Funciones Benchmark](#funciones-benchmark)
- [Configuración de Rutas de Salida](#configuración-de-rutas-de-salida)
  - [Parámetros de Rutas](#parámetros-de-rutas)
  - [Comportamiento Predeterminado de Rutas](#comportamiento-predeterminado-de-rutas)
  - [Ejemplos de Configuración de Rutas](#ejemplos-de-configuración-de-rutas)
- [Configuración de Visualizaciones](#configuración-de-visualizaciones)
  - [Parámetros de Visualización](#parámetros-de-visualización)
  - [Configuración con Valores Booleanos](#configuración-con-valores-booleanos)
    - [single\_run\_visualization](#single_run_visualization)
    - [multi\_run\_visualization](#multi_run_visualization)
  - [Configuración Manual con Diccionarios](#configuración-manual-con-diccionarios)
    - [Ejemplo de configuración individual:](#ejemplo-de-configuración-individual)
    - [Ejemplo de configuración múltiple:](#ejemplo-de-configuración-múltiple)
  - [Condiciones y Restricciones](#condiciones-y-restricciones)
    - [Restricciones por Dimensiones](#restricciones-por-dimensiones)
    - [Restricciones por Número de Ejecuciones](#restricciones-por-número-de-ejecuciones)
    - [Comportamiento Predeterminado](#comportamiento-predeterminado)
- [Ejemplo de archivo de configuración](#ejemplo-de-archivo-de-configuración)

## Requisitos

```
python >= 3.0
```

## Instalación
1. Crea un entorno virtual
  ``` shell
  # Linux
  sudo apt install python3-venv
  python3 -m venv env

  # Windows
  pip install virtualenv
  python -m venv env
  ```
2. Activa el entorno virtual  
   1. En Windows:
      ```shell
      .\env\Scripts\activate
      ```
   2. En Linux:
      ```shell
      source env/Scripts/activate
      ```

3. Instalar el paquete en modo desarrollo:

```shell
pip install -e .
```

## Desinstalación
``` sh
# Windows
pip uninstall pso-algorithm
// Eliminar los directorios .egg-info y env

# Linux
source env/Scripts/activate     # Activar el entorno virtual
pip uninstall pso-algorithm     # Eliminar dependencias
rm -rf pso_algorithm.egg-info   # Eliminar carpeta del paquete
deactivate                      # Salir del entorno virtual de python (Y si! Es 'deactivate')
rm -rf env                      # Eliminar entorno virtual
```

## Uso sugerido

### Configuración: 
- Definir los parámetros de configuración del algoritmo en un archivo JSON.
- Almacenar el archivo en la carpeta `src/tests/name.json` donde 'name' puede ser cualquier secuencia de caracteres valida.

### Ejecución: 

#### Individual (Un solo)
- Ejecutar directamente el archivo `main.py` seguido del la ruta con el archivo de configuración JSON. Por ejemplo:
    ``` shell
    python main.py src/tests/[name].json
    ```

#### Múltiple

- Ejecutar un análisis completo de todas las estrategias de peso inercial disponibles con las configuraciones integradas en el script multi_run.py
    ```shell
    python multi_run.py
    ```
- Cada estrategia donde cada estrategia tiene parametros especificos y almacena los graficos generados automaticamente para análisis.
    
    **Configuración predeterminada:**
    - Benchmarks: sphere, rastrigin, rosenbrock, griewank
    - Dimensiones: 10, 20, 30
    - Ejecuciones por configuración: 30
    - Resultados guardados en: `cases_inertia_strategies/`

### Parámetros de configuración

A continuación, se listan los parámetros por defecto que debe contener el archivo JSON. Aquellos cuyo valor predeterminado es **requerido** deben ser estrictamente especificados por el usuario.

| Parámetro                      | Tipo           | Descripción                                         | Valor predeterminado                         |
| ------------------------------ | -------------- | --------------------------------------------------- | -------------------------------------------- |
| `dimensions`                   | int            | Número de dimensiones del problema                  | **requerido**                                |
| `population_size`              | int            | Tamaño de la población                              | **requerido**                                |
| `generations`                  | int            | Número máximo de iteraciones                        | **requerido**                                |
| `benchmark`                    | string         | Función de prueba a optimizar                       | **requerido**                                |
| `bounds`                       | [float, float] | Límites inferior y superior del espacio de busqueda | **requerido**                                |
| `runs`                         | int            | Número de ejecuciones independientes                | 1                                            |
| `inertia_type`                 | float/array    | Configuración del peso inercial                     | [0.4, 0.9]                                   |
| `c1`                           | float/array    | Coeficiente cognitivo                               | **requerido** (ver detalles abajo)           |
| `c2`                           | float/array    | Coeficiente social                                  | **requerido** (ver detalles abajo)           |
| `base_output_path`             | string         | Directorio base para guardar archivos               | "output"                                     |
| `output_file`                  | string         | Nombre del archivo de resultados                    | `pso_results_{timestamp}`                    |
| `visualization_path`           | string         | Ruta para guardar visualizaciones                   | `visualization/{función_benchmark}_{timestamp}` |
| `single_run_visualization`     | bool/dict      | Activa visualizaciones para una ejecución           | false (ver detalles abajo)                   |
| `multi_run_visualization`      | bool/dict      | Activa visualizaciones para múltiples ejecuciones   | true (ver detalles abajo)                    |
| `show_individual_visualizations` | bool         | Muestra visualizaciones individuales                | true si `runs == 1`                          |
| `save_individual_visualizations` | bool         | Guarda visualizaciones individuales                 | false                                        |
| `show_multiple_visualizations` | bool           | Muestra visualizaciones múltiples                   | true si `runs > 1`                           |
| `save_multiple_visualizations` | bool           | Guarda visualizaciones múltiples                    | false                                        |
| `show_progress_bar`            | bool           | Muestra una barra de progreso                       | true                                         |
| `save_results`                 | bool           | Guarda los resultados en archivos                   | true                                         |

## Estrategias de Peso Inercial

El parámetro `inertia_type` puede configurarse de las siguientes formas:

### 1. Valor constante

```json
"inertia_type": 0.7
```

Un valor entre 0.2 y 0.9 que se utiliza como peso inercial constante.

### 2. Estrategias básicas

Ejemplo:

```json
"inertia_type": [0.4, 0.9, "linear_decreasing"]
```

Formato: `[min, max, estrategia]` donde `min` es el valor mínimo, `max` el valor máximo y `estrategia` el nombre de la estrategia a utilizar.

Estrategias disponibles:
- `linear_decreasing`: Decrecimiento lineal desde max hasta min
- `concave_decreasing`: Decrecimiento cóncavo
- `convex_decreasing`: Decrecimiento convexo
- `concave_exp_decreasing`: Decrecimiento exponencial cóncavo
- `convex_exp_decreasing`: Decrecimiento exponencial convexo
- `concave_exp_increasing`: Crecimiento exponencial cóncavo
- `convex_exp_increasing`: Crecimiento exponencial convexo
- `aleatory`: Peso aleatorio entre min y max

### 3. Estrategias avanzadas

Ejemplo:

```json
"inertia_type": [0.4, 0.9, "pso_niew"]
```

- Formato: `[min, max, estrategia]` donde `min` es el valor mínimo, `max` el valor máximo y `estrategia` el nombre de la estrategia a utilizar.
- Para PSO con Sigmoidal Inertia Weight **(pso_siw)** se debe especificar como: `[min, max, pso_siw, s]` donde `s` es el parámetro de forma sigmoidal.

Estrategias avanzadas disponibles:
- `pso_niew`: PSO con peso inercial exponencial no lineal (Natural exponential inertia
weight)
- `pso_siw`: PSO con peso inercial sigmoidal (Sugeno inertia weight)
- `de_pso`: Estrategia híbrida Evolución Diferencial-PSO (DDouble exponential adaptive inertia weight PSO)
- `gpso`: PSO Global con peso inercial creciente lineal (Guided Particle Swarm Optimization)
- `pso_tvac`: PSO con coeficientes de aceleración variables en el tiempo (Time Varying Acceleration Coefficients)

**Nota**
- `pso_tvac` se deben de definir manualmente los coeficientes c1 y c2 variables de forma creciente o descendente. Por si misma sin la especificación de estos coeficientes es 

### 4. Estrategia proopuesta híbrida con coseno

La estrategia `hybrid_cosine` permite combinar dos estrategias de peso inercial diferentes como se muestra en la siguiente formula que la define:

**Fórmula:** `P(k) = [(1 + cos((k*π)/φ)/2] * g(k) + [(1 - cos((k*π)/φ)/2] * h(k)`

donde:
- `k` es la iteración actual
- `g(k)` y `h(k)` son dos estrategias de peso inercial diferentes que reciben como principal parámetro la iteración actual. Aún que estas funciones pueden recibir más parametros en caso de ser necesarios según su definición. Por ejemplo, algunas estrategias adémas de la iteración actual, también consideran el numero de generaciones, rangos mínimo y máximo del peso inercial, entre otros.

**Formato para usarla:** `[min, max, "hybrid_cosine", strategy1_name, strategy1_params..., "SEP", strategy2_name, strategy2_params...]`

**Ejemplos:**

```json
"inertia_type": [0.4, 0.9, "hybrid_cosine", "linear_decreasing", "SEP", "dsi_pso", 2.0]
```
- En este caso, `linear_decreasing` no tiene parametros adicionales. Sin embargo, dsi_pso si, y este es su parámetro de sensibilidad.

```json
"inertia_type": [0.4, 0.9, "hybrid_cosine", "pso_niew", "SEP", "linear_decreasing"]
```

**Notas importantes:**
- Use `"SEP"` como separador entre las dos estrategias
- Cada estrategia puede tener sus propios parámetros específicos
- Si una estrategia requiere información de partículas (como `dsi_pso`), la estrategia híbrida también la requerirá
- Para estrategias constantes, especifique el valor después del nombre: `"constant", 0.7`

### 5. Estrategias adaptativas

DSI-PSO (Distance-Dependent Sigmodal Inertia) es la única estrategía adaptativa

```json
"inertia_type": [min, max, "dsi_pso", sensibilidad]
```

- **sensibilidad**: Factor de sensibilidad.

## Estrategias de Coeficientes

Los parámetros `c1` (coeficiente cognitivo) y `c2` (coeficiente social) pueden configurarse de manera similar:

### 1. Valor constante

```json
"c1": 2.0,
"c2": 2.0
```

### 2. Estrategias dinámicas

```json
"c1": [1.5, 2.5, "decreasing"],
"c2": [1.5, 2.5, "increasing"]
```

Formato: `[min, max, estrategia]`

Estrategias disponibles:
- `decreasing`: Decrecimiento lineal desde max hasta min
- `increasing`: Crecimiento lineal desde min hasta max
- `random`: Valor aleatorio entre min y max en cada iteración

## Funciones Benchmark

Funciones disponibles:
- `sphere`: Función esférica (unimodal)
- `rastrigin`: Función de Rastrigin (multimodal)
- `rosenbrock`: Función de Rosenbrock (multimodal)
- `griewank`: Función de Griewank (multimodal)

## Configuración de Rutas de Salida

El sistema permite personalizar dónde se guardan los resultados y visualizaciones mediante tres parámetros principales de rutas en el archivo JSON.

### Parámetros de Rutas

| Parámetro              | Tipo   | Descripción                                              | Valor predeterminado                    |
| ---------------------- | ------ | -------------------------------------------------------- | --------------------------------------- |
| base_output_path       | string | Directorio base donde se guardan todos los archivos     | "output"                                |
| output_file            | string | Nombre del archivo de resultados (sin extensión)        | "pso_results_YYYYMMDD_HHMMSS"          |
| visualization_path     | string | Ruta completa para guardar visualizaciones              | "{base_output_path}/visualizations/{output_file}" |

### Comportamiento Predeterminado de Rutas

**Generación automática de nombres:**
- Si no se especifica `output_file`, se genera automáticamente con formato: `pso_results_YYYYMMDD_HHMMSS`
- Si no se especifica `visualization_path`, se construye automáticamente como: `{base_output_path}/visualizations/{output_file}`

**Estructura de directorios resultante:**
```
{base_output_path}/
├── {output_file}.json              # Archivo de resultados
└── visualizations/
    └── {output_file}/               # Carpeta de visualizaciones
        ├── best_fitness_*.png
        ├── diversity_*.png
        └── ...
```

### Ejemplos de Configuración de Rutas

**Configuración básica:**
```json
{
  "base_output_path": "experimentos",
  "output_file": "experimento_sphere_dim10"
}
```
*Resultado:* Archivos en `experimentos/experimento_sphere_dim10.json` y visualizaciones en `experimentos/visualizations/experimento_sphere_dim10/`

**Configuración con ruta personalizada de visualizaciones:**
```json
{
  "base_output_path": "resultados",
  "output_file": "prueba_rastrigin",
  "visualization_path": "graficos/rastrigin_test"
}
```
*Resultado:* Archivos en `resultados/prueba_rastrigin.json` y visualizaciones en `graficos/rastrigin_test/`

**Configuración automática (solo directorio base):**
```json
{
  "base_output_path": "datos"
}
```
*Resultado:* Archivos con nombres automáticos tipo `datos/pso_results_20240315_143025.json` y visualizaciones en `datos/visualizations/pso_results_20240315_143025/`

## Configuración de Visualizaciones

El sistema de visualización permite controlar qué gráficos se generan tanto para ejecuciones individuales como para múltiples ejecuciones.

### Parámetros de Visualización

| Parámetro                        | Tipo     | Descripción                                         | Valor predeterminado       |
| -------------------------------- | -------- | --------------------------------------------------- | -------------------------- |
| single_run_visualization         | bool/dict| Configuración de gráficos para ejecución individual| false                      |
| multi_run_visualization          | bool/dict| Configuración de gráficos para múltiples ejecuciones| true                      |
| show_individual_visualizations   | bool     | Mostrar visualizaciones individuales                | true si runs == 1          |
| save_individual_visualizations   | bool     | Guardar visualizaciones individuales                | false                      |
| show_multiple_visualizations     | bool     | Mostrar visualizaciones de múltiples ejecuciones   | true si runs > 1           |
| save_multiple_visualizations     | bool     | Guardar visualizaciones de múltiples ejecuciones   | false                      |

### Configuración con Valores Booleanos

#### single_run_visualization

Cuando se establece como `true`, se activan **todas** las visualizaciones de ejecución individual disponibles:

```json
"single_run_visualization": true
```

**Visualizaciones activadas automáticamente:**
- `best_fitness`: Convergencia de la mejor aptitud (siempre disponible)
- `inertia_weight`: Evolución del peso inercial (siempre disponible)
- `particles_2d`: Distribución de partículas (**solo si dimensions == 2**)
- `surface_3d`: Superficie de la función objetivo (**solo si dimensions == 2**)
- `diversity`: Diversidad en posición, velocidad, aptitud y componente cognitiva (siempre disponible)

#### multi_run_visualization

Cuando se establece como `true`, se activan **todas** las visualizaciones de múltiples ejecuciones disponibles (**solo si runs > 1**):

```json
"multi_run_visualization": true
```

**Visualizaciones activadas automáticamente:**
- `best_run_fitness`: Mejor aptitud en la mejor ejecución
- `best_run_inertia`: Peso inercial de la mejor ejecución
- `best_fitness_per_run`: Mejores fitness obtenidos por cada ejecución
- `avg_fitness_per_run`: Historial de fitness promedio por ejecución
- `diversity`: Diversidad agregada de múltiples ejecuciones

### Configuración Manual con Diccionarios

Para control granular, puedes especificar exactamente qué visualizaciones activar:

#### Ejemplo de configuración individual:

```json
"single_run_visualization": {
    "best_fitness": true,
    "inertia_weight": true,
    "particles_2d": true,
    "surface_3d": false,
    "diversity": true
}
```

#### Ejemplo de configuración múltiple:

```json
"multi_run_visualization": {
    "best_run_fitness": true,
    "best_run_inertia": false,
    "best_fitness_per_run": true,
    "avg_fitness_per_run": true,
    "diversity": false
}
```

### Condiciones y Restricciones

#### Restricciones por Dimensiones
- **`particles_2d`** y **`surface_3d`**: Solo disponibles cuando `dimensions == 2`
- Resto de visualizaciones: Disponibles para cualquier número de dimensiones

#### Restricciones por Número de Ejecuciones
- **Visualizaciones individuales**: Siempre disponibles independientemente del valor de `runs`
- **Visualizaciones múltiples**: Solo disponibles cuando `runs > 1`

#### Comportamiento Predeterminado
- Si `runs == 1`: 
  - `show_individual_visualizations = true`
  - `show_multiple_visualizations = false`
- Si `runs > 1`:
  - `show_individual_visualizations = false` 
  - `show_multiple_visualizations = true`

## Ejemplo de archivo de configuración

```json
{
    "dimensions": 10,
    "population_size": 30,
    "generations": 100,
    "benchmark": "sphere",
    "bounds": [-5.0, 5.0],
    "runs": 5,
    "inertia_type": [0.4, 0.9, "dsi_pso", 0.5],
    "c1": 2.0,
    "c2": 2.0,
    "multi_run_visualization": {
        "best_run_fitness": true,
        "best_fitness_per_run": true,
        "avg_fitness_per_run": false,
        "diversity": true
    },
    "save_multiple_visualizations": true,
    "save_results": true
}
```
> [!TIP] Parámetro runs
El parámetro `runs` define el número de veces que se ejecutará el algoritmo bajo los mismos parámetros de configuración