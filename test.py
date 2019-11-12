import glfw


# Initializing glfw library
if not glfw.init():
    raise Exception("Glfw can not be initialazed!")

# Creating the window
window = glfw.create_window(1080, 640, "My OpenGl Window", None, None)

# Check if the window was created
if not window:
    glfw.terminate()
    raise Exception('Glfw can not be created!')

# Set window's position
glfw.set_window_pos(window, 400, 200)

# Make the context current
glfw.make_context_current(window)

# The main aplication loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glfw.swap_buffers(window)

# Terminate glfw, free alocated resources
glfw.terminate()
