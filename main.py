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
        draw.line((tuple(point[i[0]]), tuple(point[i[1]])), width=width, fill=(255,255,255))


def generate(img_size: tuple[int,int], points: list, fraction: float, draw: ImageDraw.ImageDraw, width: int, recersion: int) -> None:
    if recersion > 0:
        point_connections = [[x,(x+1)%len(points)] for x in range(len(points))]
        draw_connections(points, point_connections, draw, width)
        points = create_new_points(points, point_connections, fraction)
        far_enough = False
        for i in points[1::]:
            if ((i[0]-points[0][0])**2+(i[1]-points[0][1])**2)**0.5 > 5:
                far_enough = True
        if far_enough:
            generate(img_size, points, fraction, draw, width, recersion - 1)


def main(size: tuple, fraction: float, recersion_limit: int):
    r_size = (size[0]*10,size[1]*10)
    img = Image.new("RGBA", r_size, (0,0,0))
    draw = ImageDraw.Draw(img,)

    DT = Delaunay2D()

    points = [[0, 0], [r_size[0]-1, 0], [r_size[0]-1, r_size[1]-1], [0, r_size[1]-1]]

    for i in range(3):
        while True:
            point = [random.randint(r_size[0]-r_size[0]*0.75,r_size[0]*0.75),random.randint(r_size[1]-r_size[1]*0.75,r_size[1]*0.75)]
            toclose = False
            for i in points:
                if ((i[0]-point[0])**2+(i[1]-point[1])**2)**0.5 < max(r_size)*0.2:
                    toclose = True
            if not toclose:
                break
        points.append(point)

    DT.addPoints(points)

    shapes = DT.exportDT()

    for shape in shapes:
        generate(r_size, shape, fraction, draw, 20, recersion_limit)

    img.thumbnail(size,Image.Resampling.HAMMING)

    img.show()


main((400, 600), 0.1, 10)
