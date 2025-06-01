#version 430

layout (
    local_size_x = 8, 
    local_size_y = 8, 
    local_size_z = 8
) in;

ivec3 id = ivec3(gl_GlobalInvocationID.xyz);

layout (binding = 1, rgba32f) uniform image3D cloud;

vec3 res = vec3(100, 100, 100);
    
//==========================================================================================
// hashes
//==========================================================================================

vec3 hash3( vec3 p ) {
    const vec3 k = vec3( 0.3183099, 0.3678794, 0.3912328 );
    const vec3 l = vec3( 0.7282099, 0.8135214, 0.6952588 );
    float n = 111.0*p.x + 113.0*p.y + 117.0*p.z;
    return fract(n*fract(k*n*fract(l*n)));
}

void main() {
    vec3 col = hash3(vec3(id));
    imageStore(cloud, id, vec4(col, 1.0));
}

