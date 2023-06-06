from vispy import app, gloo
import numpy as np
from vispy.util.transforms import rotate, translate, perspective


class Apka(app.Canvas):
    def __init__(self):
        super().__init__(title="Kostka Rubika", size=(800, 800))
        gloo.set_state(depth_test=True)

        self.vertex_shader = self.load_shader("vertex_shader.glsl")
        self.fragment_shader = self.load_shader("fragment_shader.glsl")

        self.shapes = []
        self.translations = []
        self.perspektywa = 0
        self.block = False
        self.obrx = 0
        self.obry = 0
        self.obrW = rotate(0, (0, 1, 0))
        self.gen_scene()
        self.time = 0
        self.timer = app.Timer(1 / 60, connect=self.on_timer)
        self.timer.start()
        self.view = translate((self.perspektywa, 0, -8))
        self.projection = perspective(80, 1, 2, 10)
        self.model = np.eye(4, dtype=np.float32)

    def gen_scene(self):
        # model kostki
        self.shapes.append(self.gen_cube())
        self.translations.append((0, 0, 1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((0, 1.05, 1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((0, -1.05, 1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((1.05, 0, 1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((1.05, 1.05, 1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((1.05, -1.05, 1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.05, 0, 1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.05, 1.05, 1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.05, -1.05, 1.05))

        self.shapes.append(self.gen_cube())
        self.translations.append((0, 0, -1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((0, 1.05, -1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((0, -1.05, -1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((1.05, 0, -1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((1.05, 1.05, -1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((1.05, -1.05, -1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.05, 0, -1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.05, 1.05, -1.05))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.05, -1.05, -1.05))

        self.shapes.append(self.gen_cube())
        self.translations.append((0, 1.05, 0))
        self.shapes.append(self.gen_cube())
        self.translations.append((0, -1.05, 0))
        self.shapes.append(self.gen_cube())
        self.translations.append((1.05, 0, 0))
        self.shapes.append(self.gen_cube())
        self.translations.append((1.05, 1.05, 0))
        self.shapes.append(self.gen_cube())
        self.translations.append((1.05, -1.05, 0))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.05, 0, 0))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.05, 1.05, 0))
        self.shapes.append(self.gen_cube())
        self.translations.append((-1.05, -1.05, 0))

    def gen_cube(self):
        shape = dict()
        shape['program'] = gloo.Program(self.vertex_shader, self.fragment_shader, 24)

        # Generowanie płaszczyzn
        colors = np.array([
            # Ścianka 1 (przednia)
            [1, 0, 0, 0],  # Czerwony
            [1, 0, 0, 0],  # Czerwony
            [1, 0, 0, 0],  # Czerwony
            [1, 0, 0, 0],  # Czerwony
            # Ścianka 2 (tylna)
            [0, 1, 0, 0],  # Zielony
            [0, 1, 0, 0],  # Zielony
            [0, 1, 0, 0],  # Zielony
            [0, 1, 0, 0],  # Zielony
            # Ścianka 3 (lewa)
            [0, 0, 1, 0],  # Niebieski
            [0, 0, 1, 0],  # Niebieski
            [0, 0, 1, 0],  # Niebieski
            [0, 0, 1, 0],  # Niebieski
            # Ścianka 4 (prawa)
            [1, 1, 0, 0],  # Żółty
            [1, 1, 0, 0],  # Żółty
            [1, 1, 0, 0],  # Żółty
            [1, 1, 0, 0],  # Żółty
            # Ścianka 5 (górna)
            [1, 0, 1, 0],  # Magenta
            [1, 0, 1, 0],  # Magenta
            [1, 0, 1, 0],  # Magenta
            [1, 0, 1, 0],  # Magenta
            # Ścianka 6 (dolna)
            [0, 1, 1, 0],  # Cyjan
            [0, 1, 1, 0],  # Cyjan
            [0, 1, 1, 0],  # Cyjan
            [0, 1, 1, 0]  # Cyjan
        ], dtype=np.float32)

        positions = np.array([
            [-0.5, -0.5, -0.5],  # Wierzchołek 0
            [0.5, -0.5, -0.5],  # Wierzchołek 1
            [0.5, 0.5, -0.5],  # Wierzchołek 2
            [-0.5, 0.5, -0.5],  # Wierzchołek 3

            [-0.5, -0.5, 0.5],  # Wierzchołek 4
            [0.5, -0.5, 0.5],  # Wierzchołek 5
            [0.5, 0.5, 0.5],  # Wierzchołek 6
            [-0.5, 0.5, 0.5],  # Wierzchołek 7

            [-0.5, 0.5, 0.5],  # Wierzchołek 8
            [-0.5, -0.5, 0.5],  # Wierzchołek 9
            [-0.5, -0.5, -0.5],  # Wierzchołek 10
            [-0.5, 0.5, -0.5],  # Wierzchołek 11

            [0.5, 0.5, 0.5],  # Wierzchołek 8
            [0.5, -0.5, 0.5],  # Wierzchołek 9
            [0.5, -0.5, -0.5],  # Wierzchołek 10
            [0.5, 0.5, -0.5],  # Wierzchołek 11

            [0.5, -0.5, 0.5],  # Wierzchołek 16
            [0.5, -0.5, -0.5],  # Wierzchołek 17
            [-0.5, -0.5, -0.5],  # Wierzchołek 18
            [-0.5, -0.5, 0.5],  # Wierzchołek 19

            [0.5, 0.5, 0.5],  # Wierzchołek 16
            [0.5, 0.5, -0.5],  # Wierzchołek 17
            [-0.5, 0.5, -0.5],  # Wierzchołek 18
            [-0.5, 0.5, 0.5],  # Wierzchołek 19
        ], dtype=np.float32)

        # Macierz przechowująca indeksy wierzchołków, które tworzą ścianki sześcianu
        indices = np.array([
            # Ścianka 1 (przednia)
            [0, 1, 2],
            [2, 3, 0],
            # Ścianka 2 (tylna)
            [4, 5, 6],
            [6, 7, 4],
            # Ścianka 3 (lewa)
            [8, 9, 10],
            [10, 11, 8],
            # Ścianka 4 (prawa)
            [12, 13, 14],
            [14, 15, 12],
            # Ścianka 5 (górna)
            [16, 17, 18],
            [18, 19, 16],
            # Ścianka 6 (dolna)
            [20, 21, 22],
            [22, 23, 20]
        ], dtype=np.uint32)

        shape['program']['pos'] = positions
        shape['program']['color'] = colors
        shape['triangle_indices'] = gloo.IndexBuffer(indices)

        return shape

    @staticmethod
    def load_shader(shader_path):
        with open(shader_path, "r") as file:
            shader = file.read()
        return shader

    def on_draw(self, event):
        gloo.clear()
        for shape, trans in zip(self.shapes, self.translations):
            shape['program']['obr'] = rotate(0, (1, 0, 0)).dot(rotate(0, (0, 1, 0)))
            shape['program']['obr'] = self.obrW
            self.draw_shape(shape, trans)
        # i = 0
        # for shape, trans in zip(self.shapes, self.translations):
        #     if i < 5:
        #         shape['program']['obr'] = rotate(0, (1, 0, 0)).dot(rotate(0, (0, 1, 0)))
        #     else:
        #         shape['program']['obr'] = self.obrW
        #     i += 1
        #     self.draw_shape(shape, trans)

    def draw_shape(self, shape, translation=(0, 0, 0)):
        shape['program']['view'] = self.view
        shape['program']['projection'] = self.projection
        shape['program']['model'] = self.model.dot(translate(translation))
        shape['program'].draw('triangles', shape['triangle_indices'], 36)

    def on_key_press(self, event):
        shape = dict()
        if event.key == "S":
            self.obrx -= 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "D":
            self.obry += 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "W":
            self.obrx += 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "A":
            self.obry -= 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "B":
            if not self.block:
                self.block = True
            else:
                self.block = False

    def on_timer(self, event):
        if not self.block:
            self.time += 1 / 60
            self.view = rotate(self.time*180/np.pi, (0, 1, 0)).dot(translate((0, 0, -8)))
        self.show()


apka = Apka()
app.run()
