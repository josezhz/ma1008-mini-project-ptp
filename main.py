import turtle as t
import math

screen = t.Screen()
screen.setup(500, 500)
x_min, y_min, x_max, y_max = 0, 0, 100, 100
screen.setworldcoordinates(x_min, y_min, x_max, y_max)
screen.colormode(255)
t.speed(0)

def init():
  t.penup()
  t.goto(x_min, y_min)
  t.pendown()
  t.goto(x_max, y_min)
  t.goto(x_max, y_max)
  t.goto(x_min, y_max)
  t.goto(x_min, y_min)
init()

vertices = [(50, 20), (70, 30), (80, 50), (70, 70), (50, 30), (30, 70), (20, 50), (30, 30)]
vertices = []
while True:
  x = float(input('x = '))
  y = float(input('y = '))
  vertices.append((x, y))
  addVertex = int(input("add one more vertex? 1: yes 0: no"))
  if not addVertex:
    break
def drawPolygon(vertices):
  t.penup()
  t.goto(vertices[-1])
  t.pendown()
  for vertex in vertices:
    t.goto(vertex)
drawPolygon(vertices)

hatchLineData = {"angle": 45, "spacing": 2, "color": "red"}
def drawHatchLines(hatchLineData):
  [angle, spacing, color] = hatchLineData.values()
  angle = angle * math.pi / 180
  numOfHatchLines = math.floor(100 * math.sqrt(2) * math.sin(abs(angle) + math.pi / 4) / spacing) # Calculate the number of hatch lines the screen can contain
  for i in range(- numOfHatchLines, numOfHatchLines + 1):
    start_hatch = (0, i * (spacing / math.cos(angle)))
    direction_hatch = (1, math.tan(angle))
    intersections = []
    for i in range(len(vertices)):
      start_edge = vertices[i]
      nextIndex = i + 1 if i < len(vertices) - 1 else 0
      direction_edge = (vertices[nextIndex][0] - vertices[i][0], vertices[nextIndex][1] - vertices[i][1])
      A1x, A1y = start_hatch
      V1x, V1y = direction_hatch
      A2x, A2y = start_edge
      V2x, V2y = direction_edge
      t1 = ((A2x*V2y - A2y*V2x) - (A1x*V2y - A1y*V2x)) / (V1x*V2y - V1y*V2x) # t value for the hatch line equation
      t2 = ((A2x*V1y - A2y*V1x) - (A1x*V1y - A1y*V1x)) / (V1x*V2y - V1y*V2x) # t value for the edge equation
      if 0 <= t2 <= 1: # If the intersection lies within the edge
        intersection = (A1x + V1x * t1, A1y + V1y*t1)
        intersections.append(intersection)
    def getIndex0(x): return x[0]
    intersections.sort(key=getIndex0)
    if len(intersections):
      for i in range(len(intersections)):
        if i % 2 == 0:
          t.penup()
          t.goto(intersections[i])
          t.pendown()
          t.pencolor(color)
          t.goto(intersections[i + 1])
drawHatchLines(hatchLineData)

screen.exitonclick()
t.done()