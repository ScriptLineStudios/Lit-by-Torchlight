#version 330 core

in vec3 fragmentColor;
in vec2 fragmentTexCoord;

out vec4 color;

uniform sampler2D imageTexture;
uniform int random;

void main() {
    vec2 v_text2 = fragmentTexCoord;

    float c = 1.1 - (abs(v_text2.x - 0.5) + abs(v_text2.y - 0.5)) * 1.3;

    float pixelWidth = 1.0/float(random);

    float x = floor(v_text2.x/pixelWidth)*pixelWidth + pixelWidth/2.0;
    float y = floor(v_text2.y/pixelWidth)*pixelWidth + pixelWidth/2.0;

    //gl_FragColor = texture2D(Texture0, vec2(x, y));

    color = vec4(texture(imageTexture, vec2(x, y)).rgb*c, 1.0);


}
