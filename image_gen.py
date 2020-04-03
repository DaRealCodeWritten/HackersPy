from PIL import Image, ImageDraw, ImageFont
import math
from collections import deque
import os

def get_point(point, dist, f):
    # x^2 + y^2 = dist^2
    # tan(angle)^2 = y^2/x^2
    # --> x^2 + x^2 * tan^2 = dist^2
    angle = 0.0
    if f in range(0,90): angle = 90.0 - f
    elif f in range(90,180): angle = f - 90.0
    elif f in range(180,270): angle = 270.0 - f
    else: angle = f - 270.0 
    tan = float(math.tan(math.radians(angle)))
    x2 = float(dist * dist / (tan * tan + 1))
    x = float(x2 ** 0.5)
    y = float(x * tan)
    if f in range(0,90): return (point[0] + x, point[1] + y)
    elif f in range(90,180): return (point[0] - x, point[1] + y)
    elif f in range(180,270): return (point[0] - x, point[1] - y)
    else: return (point[0] + x, point[1] - y)

def ellipse(point):
    return (point[0] - 20, point[1] - 20, point[0] + 20, point[1] + 20)

def generate_image(connections):
    img = Image.new('RGB', (2000, 2000), (255, 255, 255))
    print(img.format, img.size, img.mode)
    draw = ImageDraw.Draw(img)
    position = { 'netCon': (1005, 1005) }
    #draw.ellipse((20, 20, 180, 180), fill = 'blue', outline = 'blue')
    draw.ellipse(ellipse(position['netCon']), fill = 'blue', outline = 'blue')
    queue = deque()
    nodeList = {'netCon'}
    angle = { 'netCon' : 0 }
    queue.append('netCon')
    count = 1
    for i in connections['netCon']: count = count + 1
    ang = float(180 / count)
    p = 0
    for i in connections['netCon']:
        p = p + 1
        queue.append(i)
        nodeList.add(i)
        position[i] = get_point(position['netCon'], 300, p * ang)
        draw.ellipse(ellipse(position[i]), fill = 'blue', outline = 'blue') 
        angle[i] = p * ang
    while queue:
        curNode = queue.pop()
        for i in connections[curNode]:
            if i not in nodeList:
                nodeList.add(i)
                queue.append(i)
        count = 1
        for i in connections[curNode]: count = count + 1
        ang = float(180 / count)
        p = 0
        for i in connections[curNode]: 
            if i in position:
                draw.line([position[i], position[curNode]], fill = 5, width = 5, joint = None)
            else:
                p = p + 1
                actualangle = p * ang - angle[curNode]
                if (actualangle < 0): actualangle = actualangle + 360
                position[i] = get_point(position[curNode], 300, actualangle)
                angle[i] = actualangle
                draw.ellipse(ellipse(position[i]), fill = 'blue', outline = 'blue')
                draw.line([position[i], position[curNode]], fill = 5, width = 5, joint   = None)
    font = ImageFont.truetype(os.path.join(os.getcwd(), "arial.ttf"), 72)
    for i in position:
        draw.text(position[i], i, fill=(31,117,254), font = font)
    return img