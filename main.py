import random
from PIL import Image, ImageDraw
from delaunay import Delaunay2D


def create_new_points(points: list, point_connections: list, fraction: float) -> list:
    n_points = []
    for i in point_connections:
        n_points.append(
            [
                points[i[0]][0] + (points[i[1]][0] - points[i[0]][0]) * fraction,
                points[i[0]][1] + (points[i[1]][1] - points[i[0]][1]) * fraction,
            ]
        )
    return n_points

def draw_connections(point: list, point_connections: list, draw: ImageDraw.ImageDraw, width: int) -> None:
    for i in point_connections:
        draw.line((tuple(point[i[0]]), tuple(point[i[1]])), width=width, fill=1)


def generate(points, point_connections, fraction, draw, width, recersion):
    if recersion > 0:
        draw_connections(points, point_connections, draw, width)
        points = create_new_points(points, point_connections, fraction)
        generate(points, point_connections, fraction, draw, 1, recersion - 1)


def main(size: tuple, fraction: float, recersion_limit: int):
    img = Image.new("1", size, 0)
    draw = ImageDraw.Draw(img)

    DT = Delaunay2D()

    points = [[0, 0], [size[0]-1, 0], [size[0]-1, size[1]-1], [0, size[1]-1]]

    for i in range(3):
        points.append([random.randint(size[0]-size[0]*0.75,size[0]*0.75),random.randint(size[1]-size[1]*0.75,size[1]*0.75)])

    DT.addPoints(points)

    shapes = DT.exportDT()

    for shape in shapes:
        generate(shape[0], shape[1], fraction, draw, 1, recersion_limit)

    img.show()


main((400, 600), 0.1, 100)
