# Proyecto Gráficas 2

## Versión 1.0.0:
-   Dibujando un triángulo multicolor en escena usando _Modern OpenGL_.
-   By: A.L.

## Versión 1.0.1:
-   Dibujando un cuadrado usando `GL_TRIANGLE_STRIP` y añadida una función para reescalar el contenido del _viewport_ cuando se cambie el tamaño de la ventana.
-   By: A.L.

## Versión 1.0.2:
-   Dibujando el mismo cuadrado reciclando índices, usando `GL_ELEMENT_ARRAY_BUFFER`.
-   By: A.L.

## Versión 1.0.3:
-   Dibujando un cubo en lugar de un cuadrado, y haciéndolo rotar.
-   By: A.L.

## Versión 1.0.4:
-   Añadiendo texturas al cubo, estas son imágenes guardadas en la carpeta _textures_.
-   By: A.L.

## Versión 1.0.5:
-   Añadiendo perspectiva al cubo.
-   By: A.L.

## Versión 1.0.6:
-   _test.py_ -> _miauzilla.py_
-   _xd.py_ -> _test.py_
-   By: A.L.

## Versión 1.0.7:
-   Cambiando el paradigma del programa, ahora se trabaja con POO en lugar de programación estructurada. Se creó el archivo _miauzilla\_cv.py_ en el cual se utiliza el paradigma POO.
-   _test.py_ y _miazuilla.py_ conservan el paradigma de programación estructurada, utilizando _pygame_ y _glfw_ respectivamente.
-   By: A.L.

## Versión 1.0.8:
-   Creando 3 cubos que rotan en lugar de uno, estos han sido trasladados para que se puedan visualizar mejor.
-   By: A.L.

## Versión 1.0.9:
-   Versión inicial de la traslación de los cubos, ahora uno de ellos se acerca hacia la cámara para luego desaparecer.
-   Arreglado el archivo _changelog.md_.
-   By: A.L.

## Versión 1.0.9b:
-   Optimización de la renderización/traslación de los cubos, ahora se realiza con un bucle en lugar de hacerlo uno por uno.
-   By: A.L.

## Versión 1.0.10:
-   Se renderizan 30 cubos en lugar de 3.
-   Optimización del establecimiento de posiciones iniciales de los cubos y las matrices de traslación de los cubos, ahora se utiliza un bucle.
-   Eliminación temporal de la rotación.
-   Todos los cubos ahora experimentan una traslación en el eje z.
-   By: A.L.

## Versión 1.0.10b:
-   Agregada un poco de documentación.
-   Pendiente de corregir el bug de superposición de texturas.
-   By: A.L.

## Versión 1.0.11:
-   Agregado una lista que almacena las texturas `textureSurface` y otra que alse encarga demacena las texturas transformadas a bytes `textureData`.
-   Corregido el bug de superposición de texturas.
-   Añadiendo texturas de forma aleatoria a los cubos que se acercan hacia la cámara.
-   By: A.L.

## Versión 1.0.12:
-   Se agregó el objeto que representará al gato.
-   Se configuró el objeto para que el gato no se desplace a comparacion de los demás.
-   By: E.S.

## Versión 1.0.13:
-   Se agregó documentación en cada una de las clases.
-   Eliminación definitiva de la rotación de cubos.
-   Ilusión de movimiento perpetuo de los _obstáculos_ que el personaje principal debe evitar. Una vez que pasan el sistema de referencia de la cámara se redibujan.
-   By: A.L.

## Versión 1.0.13b:
-   Arreglando _.gitignore_ y eliminando archivos innecesarios.
-   Arreglando _changelog.md_ y especificando lo siguieglBindVertexArraynte, todas las versiones sin número son por defecto versiones **a**.
-   By: A.L.

## Versión 1.0.14:
-   Agregadas texturas nuevas a _textures_.
-   Agregadas nuevas constantes:
    -   `quad_vertices`, `quad_indices`.
-   Modificadas las siguientes constantes:glBindVertexArray
    -   `vertices` a `cube_vertices`.
    -   `indices` a `cube_indices`.
-   Modificada la forma en cómo se establecía la textura.
-   Modificada la clase _Shader_ para poder usar VBO y poder dibujar más de una sola figura. Por cada nueva figura que se pretenda dibujar se tendrá que usar una nueva función _vinculate_.
-   Modificada la perspectiva para renderizar adecuadamente el suelo.
-   El dibujo se hace utilizando `glBindVertexArray`.
-   Dejando de monitoriar la carpeta __\_\_pycache\_\___.
-   By: A.L.

## Versión 1.1.0:
-   Se renderiza el objeto gato usando cubos de diferentes tamaños.
-   Se implementan las escalas para los obstáculos.
-   By: E.S. 

## Versión 1.1.1:
-   Agregados eventos de teclado, tecla **ESC** y tecla **Q**:
    -   **ESC**: salir.
    -   **Q**: rotar cámara.
- By: A.L.

## Versión 1.1.2:
-   Agregados eventos de teclado, tecla **A** y tecla **D**:
    -   **A**: mover hacia la izquierda.
    -   **D**: mover hacia la derecha.
-   Pendiente de arreglar que el objeto gato no llega a mover su cabeza.
- By: A.L.

## Versión 1.1.3:
-   Agregados los choques entre el gato y los edificios.
-   Reparado el bug del desplazamiento del gato.
-   Agregado la reubicacion de los edificios al fondo.
-   Agregado el contador de cuantos edificios ha destruido.
-   By: E.S.

## Versión 1.1.4:
-   Actualización de _readme.md_.
-   Implementado el cielo, nueva función dentro de `Window`, `vinculate_sky`.
-   Importada la librería _pygame_ para implementar los sonidos.
-   Implementado sonido de fondo y sonido de choques.
-   By: A.L.

## Versión 1.2.0:
-   Implementación de sombras, se utiliza un evento de teclado, la letra **E**, para cambiar el tipo de iluminación.
-   Implementación de movimiento a partir de las teclas direccionales, además de **A**, **W**, **D** y **S**.
-   By: A.L.