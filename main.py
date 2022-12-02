import random
from PIL import Image, ImageDraw

def create_new_points(points:list, point_connections:list, fraction:float) -> list:
    n_points = []
    for i in point_connections:
        n_points.append([points[i[0]][0]+(points[i[1]][0]-points[i[0]][0])*fraction,points[i[0]][1]+(points[i[1]][1]-points[i[0]][1])*fraction])
    return n_points

def draw_connections(point:list,point_connections:list,draw:ImageDraw.ImageDraw,width:int):
    try:
        for i in point_connections:
            draw.line((tuple(point[i[0]]),tuple(point[i[1]])),width=width,fill=1)
    except:
        pass
    
def generate(points,point_connections,fraction,draw,recersion):
    if recersion > 0:
        points = create_new_points(points,point_connections,fraction)
        draw_connections(points,point_connections,draw,1)
        generate(points,point_connections,fraction,draw,recersion-1)




def main(size:tuple,fraction:float,recersion_limit:int):
    img = Image.new('1', size, 0)
    draw = ImageDraw.Draw(img)

    points = [[0,0],[size[0],0],[size[0],size[1]],[0,size[1]]]
    point_connections = [[0,1],[1,2],[2,3],[3,0]]

    draw_connections(points,point_connections,draw,10)

    generate(points,point_connections,fraction,draw,recersion_limit)

    img.show()

main((1000,1000),0.25,10)