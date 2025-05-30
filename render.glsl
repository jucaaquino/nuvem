#version 430

layout (
    local_size_x = 8, 
    local_size_y = 8, 
    local_size_z = 1
) in;

ivec2 id = ivec2(gl_GlobalInvocationID.xy);

layout (binding = 0, rgba32f) uniform image2D target;

vec2 res = vec2(1000, 1000);

void main() {
    imageStore(target, id, vec4(1.0));
}


