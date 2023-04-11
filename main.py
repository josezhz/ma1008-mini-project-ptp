import turtle as t
import math

sc = t.Screen()
sc.setup(500, 500)
x_min, y_min, x_max, y_max = 0, 0, 100, 100
sc.setworldcoordinates(x_min, y_min, x_max, y_max)
sc.colormode(255)
t.speed(0)

def init():
  t.penup()
  t.goto(x_min, y_min)
  t.pendown()
  t.goto(x_max, y_min)
  t.goto(x_max, y_max)
  t.goto(x_min, y_max)
  t.goto(x_min, y_min)

def getPolygonData():
  vertices = []
  while True:
    vertexNo = len(vertices) + 1
    x = float(sc.numinput(f"Vertex No.{vertexNo}", (("Existing vertices:\n" + "".join([str(v) + "\n" for v in vertices])) if len(vertices) else "") + f"x{vertexNo} = ", minval=0, maxval=100))
    y = float(sc.numinput(f"Vertex No.{vertexNo}", (("Existing vertices:\n" + "".join([str(v) + "\n" for v in vertices])) if len(vertices) else "") + f"y{vertexNo} = ", minval=0, maxval=100))
    vertices.append((x, y))
    if vertexNo >= 3:
      addVertex = int(sc.numinput("Add vertex?", "1: Yes\n0: No", minval=0, maxval=1))
      if not addVertex:
        break
  holes = []
  while True:
    holeVertices = []
    while True:
      holeVertexNo = len(holeVertices) + 1
      x = float(sc.numinput(f"Hole Vertex No.{holeVertexNo}", (("Existing hole vertices:\n" + "".join([str(v) + "\n" for v in holeVertices])) if len(holeVertices) else "") + f"x{holeVertexNo} = ", minval=0, maxval=100))
      y = float(sc.numinput(f"Hole Vertex No.{holeVertexNo}", (("Existing hole vertices:\n" + "".join([str(v) + "\n" for v in holeVertices])) if len(holeVertices) else "") + f"y{holeVertexNo} = ", minval=0, maxval=100))
      holeVertices.append((x, y))
      if holeVertexNo >= 3:
        addHoleVertex = int(sc.numinput("Add hole vertex?", "1: Yes\n0: No", minval=0, maxval=1))
        if not addHoleVertex:
          holes.append(holeVertices)
          break
    addHole = int(sc.numinput("Add hole?", "1: Yes\n0: No", minval=0, maxval=1))
    if not addHole:
      break
  return {"vertices": vertices, "holes": holes}

def getHatchLineData():
  angle = float(sc.numinput("Hatch Line Angle", "unit: degree", minval=-89.99999999, maxval=89.99999999))
  spacing = float(sc.numinput("Hatch Line Spacing", "Hatch line spacing =", minval=0))
  colorMode = int(sc.numinput("Hatch Line Color Mode", "1: text (eg. red)\n2: RGB (eg. (255, 0, 0))\n3: HEX (eg. #ff0000)"))
  if colorMode == 2:
    r = int(sc.numinput("Hatch Line Color", "R =", minval=0, maxval=255))
    g = int(sc.numinput("Hatch Line Color", "G =", minval=0, maxval=255))
    b = int(sc.numinput("Hatch Line Color", "B =", minval=0, maxval=255))
    color = (r, g, b)
  else:
    color = sc.textinput("Hatch Line Color", "eg. " + ("red" if colorMode == 1 else "#ff0000"))
  return {"angle": angle, "spacing": spacing, "color": color}
        
def draw(polygonData, hatchLineData):
  # Draw Polygon
  polygons = [polygonData["vertices"]] + [i for i in polygonData["holes"]]
  for p in polygons:
    t.penup()
    t.goto(p[-1])
    t.pendown()
    for v in p:
      t.goto(v)
  # Draw Hatch Line
  [angle, spacing, color] = hatchLineData.values()
  angle = angle * math.pi / 180
  if angle == 0:
    angle = 0.000000001
  numOfHatchLines = math.floor(100 * math.sqrt(2) * math.sin(abs(angle) + math.pi / 4) / spacing) # Calculate the number of hatch lines the screen can contain
  for i in range(- numOfHatchLines, 1):
    start_hatch = (100 if angle > 0 else 0, - i * (spacing / math.cos(angle))) # Determine A1
    direction_hatch = (1, math.tan(angle)) # Determine V1
    intersections = []
    for p in polygons:
      for i in range(len(p)):
        start_edge = p[i] # Determine A2
        nextIndex = i + 1 if i < len(p) - 1 else 0
        direction_edge = (p[nextIndex][0] - p[i][0], p[nextIndex][1] - p[i][1]) # Determine V2
        A1x, A1y = start_hatch
        V1x, V1y = direction_hatch
        A2x, A2y = start_edge
        V2x, V2y = direction_edge
        t2 = ((A2x*V1y - A2y*V1x) - (A1x*V1y - A1y*V1x)) / (V1x*V2y - V1y*V2x) # t value for the edge equation
        if 0 <= t2 < 1: # If the intersection lies within the edge
          intersection = (A2x + V2x * t2, A2y + V2y*t2)
          intersections.append(intersection)
    intersections.sort()
    if len(intersections):
      for i in range(0, len(intersections) - 1, 2):
        t.penup()
        t.goto(intersections[i])
        t.pendown()
        t.pencolor(color)
        t.goto(intersections[i + 1])

init()
polygonData = {
  "vertices": [(50, 20), (70, 30), (80, 50), (70, 90), (50, 50), (30, 90), (20, 50), (30, 30)],
  "holes": [[(25, 50), (45, 50), (30, 80)], [(30, 40), (70, 40), (50, 25)]]
}
# polygonData = getPolygonData()
hatchLineData = {"angle": 30, "spacing": 1, "color": "red"}
# hatchLineData = getHatchLineData()
draw(polygonData, hatchLineData)

sc.exitonclick()
t.done()