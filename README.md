# Simulacion Ruleta
![Imagen Ruleta](ruleta.webp)
## Introducción

Este proyecto contiene un script en Python para simular tiradas de una ruleta europea.

## Uso

1. Ejecuta el script con Python:

```bash
python index.py <tiradas> <corridas> <numero elegido>
```

2. Ingresa la cantidad de tiradas que quieres simular.
3. El programa mostrará el número y color de cada tirada, y un resumen de los resultados por color.

⚠️ Asegúrate de ingresar un número de tiradas positivo, un número de corridas entre 1 y 7, y un número elegido entre 0 y 36.

### Ejemplo de uso

```bash
python index.py 1000 6 17
```

## Estadísticas reflejadas
El programa muestra las siguientes estadísticas:
* Frecuencia relativa del número elegido.
* Valor promedio acumulado en funcion de las tiradas.
* Desvío estándar acumulado en función de las tiradas.
* Varianza acumulada en función de las tiradas.
* Cantidad de veces que salió cada número en cada corrida.

Cada uno de los gráficos compara los resultados entre todas las corridas.
Cada uno también compara los resultados obtenidos para cada corrida con las estadísticas teóricas correspondientes de la ruleta europea.

