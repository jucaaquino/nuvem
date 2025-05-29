import glfw
from OpenGL.GL import *
import numpy as np
import math
from PIL import Image

VERT_SOURCE = """
#version 460 core 

layout (location = 0) in vec2 pos;

out vec2 uv;

void main() {
    gl_Position = vec4(pos * 2.0 - 1.0, 1.0, 1.0);
    uv = pos;
}
"""

FRAG_SOURCE = """
#version 460 core

layout (binding = 0) uniform sampler2D target_sampler;

in vec2 uv;
out vec4 color;

void main() {
    if (uv.x < 0.5)
        color = texture(target_sampler, uv);
    else
        color = vec4(1.0);
}
"""

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(700, 700, "nuvem", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    vertices = (
        0.0, 0.0,
        0.0, 1.0,
        1.0, 1.0,
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0
    )
    vertices = np.array(vertices, dtype = np.float32)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, vertices.itemsize*2, ctypes.c_void_p(0))

    program = glCreateProgram()
    vert_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vert_shader, VERT_SOURCE)
    glCompileShader(vert_shader)
    glAttachShader(program, vert_shader)
    glDeleteShader(vert_shader)
    frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(frag_shader, FRAG_SOURCE)
    glCompileShader(frag_shader)
    glAttachShader(program, frag_shader)
    glDeleteShader(frag_shader)
    glLinkProgram(program)

    # load texture

    resolution = (1000, 1000)
     
    glActiveTexture(GL_TEXTURE0)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
     
    img = Image.open('kiki.png')
    data = img.tobytes()

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, *resolution, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glBindImageTexture(2, texture_id, 0, GL_TRUE, 0, GL_READ_WRITE, GL_RGBA32F) # may change later
   
    num_work_groups = (
        math.ceil(resolution[0] / 8),
        math.ceil(resolution[1] / 8),
        1
    )

    # setup shader

    #shader_source = open('render.glsl').read()
    #    
    #shader = glCreateShader(GL_COMPUTE_SHADER)
    #glShaderSource(shader, shader_source)
    #glCompileShader(shader)

    #ok = glGetShaderiv(shader, GL_COMPILE_STATUS)
    #if not ok:
    #    print(glGetShaderInfoLog(shader).decode("utf-8"))
    #    exit()
    #            
    #shader_id = glCreateProgram()
    #glAttachShader(shader_id, shader)
    #glDeleteShader(shader)
    ##glBindAttribLocation(shader_id, 0, "target")
    #glLinkProgram(shader_id)
    
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        #glUseProgram(shader_id)

        #glDispatchCompute(*num_work_groups)
        #glMemoryBarrier(GL_SHADER_IMAGE_ACCESS_BARRIER_BIT)

        # Render here, e.g. using pyOpenGL
        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(program)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
