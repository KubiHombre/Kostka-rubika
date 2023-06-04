varying vec4 v_color;
uniform float mask;

void main() {
    gl_FragColor = mask * vec4(v_color);
}