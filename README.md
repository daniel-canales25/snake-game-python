# Snake Game

**Integrante:** Daniel Canales Taylor

**Fecha:** 20/08/2026

## Objetivo del Sistema

Desarrollar un juego clásico de la serpiente (Snake) como proyecto de la materia Lógica de Programación, aplicando programación orientada a objetos, manejo de estados y persistencia de datos con Python y Pygame.

## Descripción de Funcionalidades

- **Pantalla de inicio:** Muestra una tabla de las mejores puntuaciones (top 10) y un botón PLAY para iniciar el juego.
- **Movimiento de la serpiente:** Control mediante teclas flechas (arriba, abajo, izquierda, derecha); el sistema rechaza giros de 180° para evitar colisión inmediata.
- **Comida:** Aparece aleatoriamente en el grid, sin superponerse al cuerpo de la serpiente. Cada alimento consumido suma 10 puntos e incrementa el tamaño de la serpiente.
- **Colisiones:** El juego termina si la serpiente colisiona con las paredes, consigo misma o se sale del área del grid.
- **Persistencia de puntuaciones:** Las puntuaciones se guardan automáticamente en un archivo `scores.json`. Solo se mantienen las 10 mejores puntuaciones.
- **Pantalla de nombre de jugador:** Al finalizar la partida, el jugador puede ingresar su nombre (máximo 5 caracteres) para registrar su puntuación.
- **Reinicio rápido:** Desde la pantalla de nombre se puede reiniciar el juego con la tecla Espacio.

## Requisitos

- Python 3.12
- uv (gestor de dependencias)
- Pygame >= 2.6.1

## Ejecución

```sh
uv sync
uv run snake-game
```

## Documentación

- Reporte PDF
- Diagramas
- Diapositivas

``` ruta
/documentacion
```

## Video Explicativo

- Se encuentra en la raiz del proyecto

``` ruta
/
```