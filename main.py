from vispy import app, gloo
import numpy as np
from vispy.util.transforms import rotate, translate, perspective
from vispy.geometry.generation import create_box


class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title="Hello world!", size=(800, 800))
        gloo.set_state(depth_test=True)

        self.vertex_shader = self.load_shader("vertex_shader.glsl")
        self.fragment_shader = self.load_shader("fragment_shader.glsl")

        self.shapes = []
        self.translations = []
        self.perspektywa = 0

        self.gen_scene()
        self.time = 0
        self.timer = app.Timer(1 / 60, connect=self.on_timer)
        self.timer.start()
        self.view = translate((self.perspektywa, 0, -8))
        self.projection = perspective(80, 1, 2, 10)
        self.model = np.eye(4, dtype=np.float32)

    def gen_scene(self):
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.51, -1.51, 1.51))
        self.shapes.append(self.gen_cube())
        self.translations.append((-0.5, -1.51, 1.51))
        self.shapes.append(self.gen_cube())
        self.translations.append((0.51, -1.51, 1.51))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.51, -0.5, 1.51))
        self.shapes.append(self.gen_cube())
        self.translations.append((-0.5, -0.5, 1.51))
        self.shapes.append(self.gen_cube())
        self.translations.append((0.51, -0.5, 1.51))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.51, 0.51, 1.51))
        self.shapes.append(self.gen_cube())
        self.translations.append((-0.5, 0.51, 1.51))
        self.shapes.append(self.gen_cube())
        self.translations.append((0.51, 0.51, 1.51))

    def gen_cube(self):
        shape = dict()
        shape['program'] = gloo.Program(self.vertex_shader, self.fragment_shader)
        V, I, L = create_box()
        shape['program']['pos'] = V['position']
        shape['program']['color'] = V['color']
        shape['triangle_indices'] = gloo.IndexBuffer(I)
        shape['line_indices'] = gloo.IndexBuffer(L)
        return shape

    @staticmethod
    def load_shader(shader_path):
        with open(shader_path, "r") as file:
            shader = file.read()
        return shader

    def on_draw(self, event):
        gloo.clear()
        for shape, trans in zip(self.shapes, self.translations):
            self.draw_shape(shape, trans)

    def draw_shape(self, shape, translation=(0, 0, 0)):
        shape['program']['view'] = self.view
        shape['program']['projection'] = self.projection
        shape['program']['model'] = self.model.dot(translate(translation))
        shape['program']['mask'] = 1
        shape['program'].draw("triangles", shape['triangle_indices'])
        shape['program']['mask'] = 0
        shape['program'].draw("lines", shape['line_indices'])

    def on_key_press(self, event):
        if event.key == " ":
            shape = dict()
            self.perspektywa += 1
            self.view = translate((self.perspektywa, 0, -8))
            shape['program']['view'] = self.view
            self.show()

    def on_timer(self, event):
        self.time += 1 / 60
        self.model = rotate(45, (0, 1, 0))
        self.show()


apka = Apka()
app.run()
