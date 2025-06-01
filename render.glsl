#version 430

layout (
    local_size_x = 8, 
    local_size_y = 8, 
    local_size_z = 1
) in;

ivec2 id = ivec2(gl_GlobalInvocationID.xy);

layout (binding = 0, rgba32f) uniform image2D target;
layout (binding = 1) uniform sampler3D cloud_sampler;

vec2 res = vec2(1000, 1000);

void main() {
    vec2 uv = vec2(id) / res;
    vec4 col = texture(cloud_sampler, vec3(uv, 0.5));

    imageStore(target, id, vec4(col));
}


