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
        self.rotations = []
        self.history = []
        self.i = 0
        self.cofanie = 0
        self.key_block = False
        for i in range(26):
            self.rotations.append(np.eye(4, dtype=np.float32))
        self.block = True
        self.obrx = 0
        self.obry = 0
        self.rot_0 = 0
        self.rot_1 = 0
        self.rot_2 = 0
        self.rot_3 = 0
        self.rot_4 = 0
        self.rot_5 = 0
        self.rot_6 = 0
        self.rot_7 = 0
        self.rot_8 = 0
        self.obrW = np.eye(4, dtype=np.float32)
        self.gen_scene()
        self.time = 0
        self.timer = app.Timer(1 / 60, connect=self.on_timer)
        self.timer.start()
        self.view = translate((0, 0, -8))
        self.projection = perspective(80, 1, 2, 10)
        self.model = np.eye(4, dtype=np.float32)
        self.cube00 = 0
        self.cube01 = 1
        self.cube02 = 2
        self.cube03 = 3
        self.cube04 = 4
        self.cube05 = 5
        self.cube06 = 6
        self.cube07 = 7
        self.cube08 = 8
        self.cube09 = 9
        self.cube10 = 10
        self.cube11 = 11
        self.cube12 = 12
        self.cube13 = 13
        self.cube14 = 14
        self.cube15 = 15
        self.cube16 = 16
        self.cube17 = 17
        self.cube18 = 18
        self.cube19 = 19
        self.cube20 = 20
        self.cube21 = 21
        self.cube22 = 22
        self.cube23 = 23
        self.cube24 = 24
        self.cube25 = 25

        self.rotate_start = False
        self.last_x = 0
        self.last_y = 0
        self.last_z = 0
        self.rotate_z = False

    def gen_scene(self):
        # model kostki

        # ścianka 0
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

        # ścianka 1
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

        # ścianka 2
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
        self.i = 0
        for shape, trans in zip(self.shapes, self.translations):
            if self.i == self.cube00:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_0, (0, 0, 1)).dot(rotate(self.rot_6, (1, 0, 0))).dot(rotate(self.rot_7, (0, 1, 0))))
            if self.i == self.cube01:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_0, (0, 0, 1)).dot(rotate(self.rot_2, (0, 1, 0))).dot(rotate(self.rot_6, (1, 0, 0))))
            if self.i == self.cube02:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_0, (0, 0, 1)).dot(rotate(self.rot_3, (0, 1, 0))).dot(rotate(self.rot_6, (1, 0, 0))))
            if self.i == self.cube03:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_0, (0, 0, 1)).dot(rotate(self.rot_4, (1, 0, 0))).dot(rotate(self.rot_7, (0, 1, 0))))
            if self.i == self.cube04:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_0, (0, 0, 1)).dot(rotate(self.rot_2, (0, 1, 0))).dot(rotate(self.rot_4, (1, 0, 0))))
            if self.i == self.cube05:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_0, (0, 0, 1)).dot(rotate(self.rot_3, (0, 1, 0))).dot(rotate(self.rot_4, (1, 0, 0))))
            if self.i == self.cube06:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_0, (0, 0, 1)).dot(rotate(self.rot_5, (1, 0, 0))).dot(rotate(self.rot_7, (0, 1, 0))))
            if self.i == self.cube07:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_0, (0, 0, 1)).dot(rotate(self.rot_2, (0, 1, 0))).dot(rotate(self.rot_5, (1, 0, 0))))
            if self.i == self.cube08:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_0, (0, 0, 1)).dot(rotate(self.rot_3, (0, 1, 0))).dot(rotate(self.rot_5, (1, 0, 0))))
            if self.i == self.cube09:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_1, (0, 0, 1)).dot(rotate(self.rot_6, (1, 0, 0))).dot(rotate(self.rot_7, (0, 1, 0))))
            if self.i == self.cube10:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_1, (0, 0, 1)).dot(rotate(self.rot_2, (0, 1, 0))).dot(rotate(self.rot_6, (1, 0, 0))))
            if self.i == self.cube11:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_1, (0, 0, 1)).dot(rotate(self.rot_3, (0, 1, 0))).dot(rotate(self.rot_6, (1, 0, 0))))
            if self.i == self.cube12:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_1, (0, 0, 1)).dot(rotate(self.rot_4, (1, 0, 0))).dot(rotate(self.rot_7, (0, 1, 0))))
            if self.i == self.cube13:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_1, (0, 0, 1)).dot(rotate(self.rot_2, (0, 1, 0))).dot(rotate(self.rot_4, (1, 0, 0))))
            if self.i == self.cube14:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_1, (0, 0, 1)).dot(rotate(self.rot_3, (0, 1, 0))).dot(rotate(self.rot_4, (1, 0, 0))))
            if self.i == self.cube15:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_1, (0, 0, 1)).dot(rotate(self.rot_5, (1, 0, 0))).dot(rotate(self.rot_7, (0, 1, 0))))
            if self.i == self.cube16:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_1, (0, 0, 1)).dot(rotate(self.rot_2, (0, 1, 0))).dot(rotate(self.rot_5, (1, 0, 0))))
            if self.i == self.cube17:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_1, (0, 0, 1)).dot(rotate(self.rot_3, (0, 1, 0))).dot(rotate(self.rot_5, (1, 0, 0))))
            if self.i == self.cube18:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_8, (0, 0, 1)).dot(rotate(self.rot_2, (0, 1, 0))).dot(rotate(self.rot_6, (1, 0, 0))))
            if self.i == self.cube19:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_8, (0, 0, 1)).dot(rotate(self.rot_2, (0, 1, 0))).dot(rotate(self.rot_6, (1, 0, 0))))
            if self.i == self.cube20:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_4, (1, 0, 0)).dot(rotate(self.rot_7, (0, 1, 0))).dot(rotate(self.rot_8, (0, 0, 1))))
            if self.i == self.cube21:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_4, (1, 0, 0)).dot(rotate(self.rot_2, (0, 1, 0))).dot(rotate(self.rot_8, (0, 0, 1))))
            if self.i == self.cube22:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_3, (0, 1, 0)).dot(rotate(self.rot_4, (1, 0, 0))).dot(rotate(self.rot_8, (0, 0, 1))))
            if self.i == self.cube23:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_5, (1, 0, 0)).dot(rotate(self.rot_7, (0, 1, 0))).dot(rotate(self.rot_8, (0, 0, 1))))
            if self.i == self.cube24:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_5, (1, 0, 0)).dot(rotate(self.rot_8, (0, 0, 1))).dot(rotate(self.rot_2, (0, 1, 0))))
            if self.i == self.cube25:
                self.rotations[self.i] = self.rotations[self.i].dot(
                    rotate(self.rot_5, (1, 0, 0)).dot(rotate(self.rot_8, (0, 0, 1))).dot(
                        rotate(self.rot_3, (0, 1, 0))))
            self.draw_shape(shape, trans)
            self.i += 1
        if self.rot_0 == 90:
            a = self.cube01
            self.cube01 = self.cube03
            b = self.cube02
            self.cube02 = self.cube06
            self.cube03 = b
            c = self.cube04
            self.cube04 = self.cube05
            self.cube05 = self.cube08
            self.cube06 = a
            d = self.cube07
            self.cube07 = c
            self.cube08 = d

        if self.rot_1 == 90:
            a = self.cube10
            self.cube10 = self.cube12
            self.cube12 = self.cube11
            b = self.cube13
            self.cube13 = self.cube14
            self.cube14 = self.cube17
            c = self.cube15
            self.cube15 = a
            d = self.cube16
            self.cube16 = b
            self.cube17 = d
            self.cube11 = c

        if self.rot_2 == 90:
            a = self.cube07
            self.cube07 = self.cube16
            b = self.cube01
            self.cube01 = self.cube24
            c = self.cube04
            self.cube04 = a
            self.cube24 = self.cube10
            self.cube10 = self.cube21
            self.cube21 = b
            self.cube16 = self.cube13
            self.cube13 = c

        if self.rot_3 == 90:
            a = self.cube08
            self.cube08 = self.cube17
            b = self.cube02
            self.cube02 = self.cube25
            d = self.cube05
            self.cube05 = a
            self.cube25 = self.cube11
            c = self.cube22
            self.cube22 = b
            self.cube17 = self.cube14
            self.cube11 = c
            self.cube14 = d

        if self.rot_4 == 90:
            a = self.cube04
            self.cube04 = self.cube13
            b = self.cube21
            self.cube21 = self.cube12
            self.cube13 = self.cube14
            c = self.cube03
            self.cube03 = b
            self.cube12 = self.cube22
            d = self.cube05
            self.cube05 = a
            self.cube22 = c
            self.cube14 = d

        if self.rot_5 == 90:
            a = self.cube07
            self.cube07 = self.cube16
            b = self.cube24
            self.cube24 = self.cube15
            self.cube16 = self.cube17
            d = self.cube06
            self.cube06 = b
            self.cube15 = self.cube25
            c = self.cube08
            self.cube08 = a
            self.cube25 = d
            self.cube17 = c

        if self.rot_6 == 90:
            a = self.cube01
            self.cube01 = self.cube10
            b = self.cube18
            self.cube18 = self.cube09
            self.cube10 = self.cube11
            c = self.cube00
            self.cube00 = b
            self.cube09 = self.cube19
            b = self.cube02
            self.cube02 = a
            self.cube19 = c
            self.cube11 = b

        if self.rot_7 == 90:
            a = self.cube06
            self.cube06 = self.cube15
            b = self.cube00
            self.cube00 = self.cube23
            d = self.cube03
            self.cube03 = a
            self.cube23 = self.cube09
            e = self.cube20
            self.cube20 = b
            self.cube15 = self.cube12
            self.cube09 = e
            self.cube12 = d

        if self.rot_8 == 90:
            a = self.cube24
            self.cube24 = self.cube21
            b = self.cube18
            self.cube18 = self.cube20
            self.cube21 = self.cube22
            c = self.cube23
            self.cube23 = b
            self.cube20 = self.cube19
            d = self.cube25
            self.cube25 = a
            self.cube19 = c
            self.cube22 = d
        if self.cofanie != 0:
            self.cofanie += 1
            if self.cofanie == 3:
                self.cofanie = 0
        else:
            self.rot_0 = 0
            self.rot_1 = 0
            self.rot_2 = 0
            self.rot_3 = 0
            self.rot_4 = 0
            self.rot_5 = 0
            self.rot_6 = 0
            self.rot_7 = 0
            self.rot_8 = 0
            self.key_block = False

    def draw_shape(self, shape, translation=(0, 0, 0)):
        shape['program']['view'] = self.view
        shape['program']['projection'] = self.projection
        shape['program']['obr'] = self.obrW
        shape['program']['model'] = self.model.dot(translate(translation).dot(self.rotations[self.i]))
        shape['program'].draw('triangles', shape['triangle_indices'], 36)

    def on_mouse_press(self, event):
        if event.button == 1:  # Lewy przycisk myszy
            self.rotate_start = True
            self.last_x = event.pos[0]
            self.last_y = event.pos[1]
        if event.button == 2 and not self.rotate_start:
            self.rotate_z = True
            self.last_z = event.pos[1]

    def on_mouse_release(self, event):
        if event.button == 1:  # Lewy przycisk myszy
            self.rotate_start = False
        if event.button == 2 and not self.rotate_start:
            self.rotate_z = False

    def on_mouse_move(self, event):
        if self.rotate_start:
            dx = (event.pos[0] - self.last_x) / 6
            dy = (event.pos[1] - self.last_y) / 6
            self.last_x = event.pos[0]
            self.last_y = event.pos[1]
            rotation = rotate(dx, (0, 1, 0)).dot(rotate(dy, (1, 0, 0)))
            self.obrW = rotation.dot(self.obrW)
        if self.rotate_z:
            dz = (event.pos[1] - self.last_z) / 6
            self.last_z = event.pos[1]
            rotation = rotate(-dz, (0, 0, 1))
            self.obrW = rotation.dot(self.obrW)

    def on_key_press(self, event):
        shape = dict()
        if event.key == "S" and not self.key_block:
            self.key_block = True
            self.obrx -= 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "D" and not self.key_block:
            self.key_block = True
            self.obry += 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "W" and not self.key_block:
            self.key_block = True
            self.obrx += 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))
        if event.key == "A" and not self.key_block:
            self.key_block = True
            self.obry -= 30
            self.obrW = rotate(self.obrx, (1, 0, 0)).dot(rotate(self.obry, (0, 1, 0)))

        if event.key == "Z" and not self.key_block:
            self.key_block = True
            self.history.append(0)
            self.rot_0 += 90
        if event.key == "X" and not self.key_block:
            self.key_block = True
            self.history.append(1)
            self.rot_1 += 90
        if event.key == "C" and not self.key_block:
            self.key_block = True
            self.history.append(2)
            self.rot_2 += 90
        if event.key == "V" and not self.key_block:
            self.key_block = True
            self.history.append(3)
            self.rot_3 += 90
        if event.key == "B" and not self.key_block:
            self.key_block = True
            self.history.append(4)
            self.rot_4 += 90
        if event.key == "N" and not self.key_block:
            self.key_block = True
            self.history.append(5)
            self.rot_5 += 90
        if event.key == "J" and not self.key_block:
            self.key_block = True
            self.history.append(6)
            self.rot_6 += 90
        if event.key == "K" and not self.key_block:
            self.key_block = True
            self.history.append(7)
            self.rot_7 += 90
        if event.key == "L" and not self.key_block:
            self.key_block = True
            self.history.append(8)
            self.rot_8 += 90
        if (event.key == "P" and not self.key_block and len(self.history) != 0) or (
                self.cofanie != 0 and not self.key_block and len(self.history)):
            self.key_block = True
            if self.history[len(self.history) - 1] == 0:
                self.rot_0 = 90
            if self.history[len(self.history) - 1] == 1:
                self.rot_1 = 90
            if self.history[len(self.history) - 1] == 2:
                self.rot_2 = 90
            if self.history[len(self.history) - 1] == 3:
                self.rot_3 = 90
            if self.history[len(self.history) - 1] == 4:
                self.rot_4 = 90
            if self.history[len(self.history) - 1] == 5:
                self.rot_5 = 90
            if self.history[len(self.history) - 1] == 6:
                self.rot_6 = 90
            if self.history[len(self.history) - 1] == 7:
                self.rot_7 = 90
            if self.history[len(self.history) - 1] == 8:
                self.rot_8 = 90
            self.history.pop()
            self.cofanie += 1
        if event.key == "Q":
            if not self.block:
                self.block = True
            else:
                self.block = False

    def on_timer(self, event):
        if not self.block:
            self.time += 1 / 60
            self.view = rotate(self.time * 180 / np.pi, (0, 1, 0)).dot(translate((0, 0, -8)))
        self.show()


apka = Apka()
app.run()
