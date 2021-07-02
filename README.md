# App Axes for dinamic  v.1.0

## Edicion, Composicion, Imagenes, Videos

> Construyendo un visor de imagenes de videos GUI en tk. Los ficheros de videos pueden ser de los formatos más comunes, .mp4, .flv, .avi, .gif ... etc,. 

> El visor axe's enlaza con los videos correspondientes en los archivos de raiz designado y almacena la última dirección de archivo vista.

## Lanzar:

Use:  `python3 flowlayout.py`

o Use:
```
$ chmod +x flowlayout.py
$ ./flowlayout.py
```

## Posible Mejoras:

>   + Configuracion parametros tamaño split's.
>	+ Análisis del costo de recurso ...
>	+ Menu popups con creación de gif del video y tambien una imagen especifica.


## Dependencias:
- Se requiere en Window tener instalado la aplicacion ffmpeg en el sistema, y configurada las rutas del mimo, ver: https://ffmpeg.org. en linux escriba:
` sudo apt install ffmpeg`.

- Tambien:
	+ tkinter GUI python3
	+ ffpyplayer
	+ PIL
	+ OpenCV