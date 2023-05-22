from vispy import app, gloo
import numpy as np


class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title='Hello world!',
                         size=(800, 800))
        self.program = None
        self.draw_square()

    def draw_square(self):
        vertex_shader = self.load_shader('vertex_shader.glsl')
        fragment_shader = self.load_shader('fragment_shader.glsl')
        self.program = gloo.Program(vertex_shader, fragment_shader, 4)
        self.program['pos'] = np.array([[-1, 1],
                                        [1, 1],
                                        [1, -1],
                                        [-1, -1]])
        self.program['color'] = np.array([[1, 0, 0],
                                         [0, 1, 0],
                                         [0, 0, 1],
                                         [1, 1, 0]])
        self.show()

    @staticmethod
    def load_shader(shader_path):
        # file = open(shader_path, 'r')
        with open(shader_path, 'r') as file:
            shader = file.read()
        return shader

    def on_draw(self, event):
        self.program.draw('triangle_fan')

    def on_key_press(self, event):
        if event.key == ' ':
            self.program['color'] = np.random.rand(3)
            self.show()


apka = Apka()
app.run()
