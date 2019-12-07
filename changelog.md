# Miauzilla's changelog

## Version 1.0.0:
-   Drawing a multicolored triangle on the scene using _Modern OpenGL_.
-   By: A.L.

## Version 1.0.1:
-   Drawing a square using `GL_TRIANGLE_STRIP` and adding a function to rescale the content of the _viewport_ when the window size is changed.
-   By: A.L.

## Version 1.0.2:
-   Drawing the same square by recycling indexes, using `GL_ELEMENT_ARRAY_BUFFER`.
-   By: A.L.

## Version 1.0.3:
-   - Drawing a cube instead of a square, and rotating it.
-   By: A.L.

## Version 1.0.4:
-   Adding textures to the cube, these are images saved in the _textures_ folder.
-   By: A.L.

## Version 1.0.5:
-   Adding perspective to the cube.
-   By: A.L.

## Version 1.0.6:
-   _test.py_ -> _miauzilla.py_
-   _xd.py_ -> _test.py_
-   By: A.L.

## Version 1.0.7:
-   Changing the paradigm of the program, now working with OOP instead of structured programming. The _miauzilla \ _cv.py_ file was created in which the OOP paradigm is used.
-   _test.py_ and _miazuilla.py_ retain the structured programming paradigm, using _pygame_ and _glfw_ respectively.
-   By: A.L.

## Version 1.0.8:
-   Creating 3 rotating cubes instead of one, they have been moved so they can visualize better.
-   By: A.L.

## Version 1.0.9:
-   Initial version of the translation of the cubes, now one of them approaches the camera and then disappears.
- Fixed the file _changelog.md_.
-   By: A.L.

## Version 1.0.9b:
-   Optimization of the rendering / translation of the cubes, now it is done with a loop instead of one by one.
-   By: A.L.

## Version 1.0.10:
-   30 cubes are rendered instead of 3.
-   Optimization of the establishment of initial positions of the cubes and the matrices of translation of the cubes, now a loop is used.
-   Temporary elimination of rotation.
-   All cubes now undergo a z-axis translation.
-   By: A.L.

## Version 1.0.10b:
-   Added some documentation.
-   Pending correction of the texture overlay error.
-   By: A.L.

## Version 1.0.11:
-   Added a list that stores the textures `textureSurface` and another that also handles the textures transformed to bytes` textureData`.
-   Fixed texture overlay error.
-   Adding textures randomly to the cubes that approach the camera.
-   By: A.L.

## Version 1.0.12:
-   Added the object that will represent the cat.
-   The object was configured so that the cat does not move to a comparison of the others.
-   By: E.S.

## Version 1.0.13:
-   Documentation was added in each of the classes.
-   Final elimination of cube rotation.
-   Illusion of perpetual movement of the obstacles that the main character should avoid. Once they pass the camera reference system they are redrawn.
-   By: A.L.

## Version 1.0.13b:
-   Arreglando _.gitignore_ y eliminando archivos innecesarios.
-   Fixing _changelog.md_ and specifying the following, all versions without number are by default versions **a**.
-   By: A.L.

## Version 1.0.14:
-   Added new textures to _textures_ folder.
-   New constants added:
    -   `quad_vertices`, `quad_indices`.
-   Modified the following constants:
    -   `vertices` a `cube_vertices`.
    -   `indices` a `cube_indices`.
-   Modified the way in which the texture was established.
-   Modified the _Shader_ class to be able to use VBO and draw more than one figure. For each new figure that is intended to be drawn, a new function _vinculate_ will have to be used.
-   The drawing is made using `glBindVertexArray`.
- Stop monitoring the __\_\_pycache\_\___ folder.
-   By: A.L.

## Version 1.1.0:
-   The cat object is rendered using cubes of different sizes.
-   The scales for obstacles are implemented.
-   By: E.S. 

## Version 1.1.1:
-   Added keyboard events, key **ESC** and **Q**:
    -   **ESC**: exit.
    -   **Q**: camera rotate.
- By: A.L.

## Version 1.1.2:
-   Added keyboard events, key **A** and **D**:
    -   **A**: move to the left.
    -   **D**: move to the right.
-   Pending to fix that the cat object does not move its head.
- By: A.L.

## Version 1.1.3:
-   Added the clashes between the cat and the buildings.
-   Fixed the error of the displacement of the cat.
-   Added the relocation of the buildings to the bottom.
-   Added the counter of how many buildings it has destroyed.
-   By: E.S.

## Version 1.1.4:
-   Update of _readme.md_.
-   Implemented the sky, new function within `Window`,` vinculate_sky`.
-   Imported the _pygame_ library to implement the sounds.
-   Implemented background sound and crash sound.
-   By: A.L.

## Version 1.2.0:
-   Shadow implementation, a keyboard event, the letter **E**, is used to change the type of lighting.
-   Implementation of movement from the arrow keys, in addition to **A**, **W**, **D** and **S**.
-   By: A.L.

## Version 1.2.0b:
-   Translating everythin from spanish to english.
-   Changing the _readme.md_ file.
-   Changing main file:
    - _miauzilla\_cv.py_ to _miauzilla.py_.
-   By: A.L.

## Version 1.2.0c:
-   Fixed _changelog.md_.
-   By: A.L.