from ursina import *

app = Ursina()

a = EditorCamera()
a.move_speed = 0

Colors = {
    'white': color.white,
    'yellow': color.yellow,
    'green': color.green,
    'blue': color.blue,
    'red': color.red,
    'orange': color.orange

}
y_layers=[]
neg_y_layers=[]
x_layers=[]
neg_x_layers=[]
z_layers=[]
neg_z_layers=[]
all_tiles=[]
pivot = Entity()
cubies = []
for x in -1,0,1:
    for y in -1,0,1:
        for z in -1,0,1:
            cubie = Entity(
                model='cube',
                color=color.black,
                position=(x, y, z),
                scale=0.98
            )
            cubies.append(cubie)

            # if y == 1:
            #     Entity(parent=cubie, model='quad', color=Colors['white'], position=(0, 0.501, 0), rotation_x=90, scale=0.88)
            # if y == -1:
            #     Entity(parent=cubie, model='quad', color=Colors['yellow'], position=(0, -0.501, 0), rotation_x=270, scale=0.88)
            # if x == 1:
            #     Entity(parent=cubie, model='quad', color=Colors['red'], position=(0.501, 0, 0), rotation_y=270, scale=0.88)
            # if x == -1:
            #     Entity(parent=cubie, model='quad', color=Colors['orange'], position=(-0.501, 0, 0), rotation_y=90, scale=0.88)
            # if z == 1:
            #     Entity(parent=cubie, model='quad', color=Colors['blue'], position=(0, 0, 0.501), rotation_y=180, scale=0.88)
            # if z == -1:
            #     Entity(parent=cubie, model='quad', color=Colors['green'], position=(0, 0, -0.501), rotation_y=0, scale=0.88)

            if y == 1:
                c = Entity(parent=cubie, model='quad', color=Colors['white'], position=(0, 0.501, 0), rotation_x=90, scale=0.88)
                y_layers.append(c)
            if y == -1:
                c = Entity(parent=cubie, model='quad', color=Colors['white'], position=(0, -0.501, 0), rotation_x=270, scale=0.88)
                neg_y_layers.append(c)
            if x == 1:
                c = Entity(parent=cubie, model='quad', color=Colors['white'], position=(0.501, 0, 0), rotation_y=270, scale=0.88)
                x_layers.append(c)
            if x == -1:
                c = Entity(parent=cubie, model='quad', color=Colors['white'], position=(-0.501, 0, 0), rotation_y=90, scale=0.88)
                neg_x_layers.append(c)
            if z == 1:
                c = Entity(parent=cubie, model='quad', color=Colors['white'], position=(0, 0, 0.501), rotation_y=180, scale=0.88)
                z_layers.append(c)
            if z == -1:
                c = Entity(parent=cubie, model='quad', color=Colors['white'], position=(0, 0, -0.501), rotation_y=0, scale=0.88)
                neg_z_layers.append(c)


STATE = 'INPUT_COLORS'
if STATE == 'INPUT_COLORS':
    for layer in (neg_z_layers, x_layers, reversed(z_layers), reversed(neg_x_layers), y_layers, neg_y_layers):
        all_tiles.extend(layer)
    tiles_index = 1
    all_tiles[0].color = color.cyan


is_rotating = False
def rotate(axis, layer, angle):
    if is_rotating:
        return

    pivot.rotation = (0, 0, 0)
    pivot.position = (0, 0, 0)

    for c in cubies:
        pos = round(c.world_position[axis])
        if pos == layer:
            c.world_parent = pivot
    rotation = [0,0,0]
    rotation[axis]+=angle
    print(rotation)
    pivot.animate_rotation(rotation, duration=0.25, curve=curve.linear)
    invoke(finish_rotation, delay=0.26)

def finish_rotation():
    global is_rotating
    for c in cubies:
        if c.world_parent == pivot:
            c.world_parent = scene
            c.position = (round(c.x), round(c.y), round(c.z))
            c.rotation = (
                round(c.rotation_x / 90) * 90,
                round(c.rotation_y / 90) * 90,
                round(c.rotation_z / 90) * 90
            )
    pivot.rotation = (0, 0, 0)
    is_rotating = False

counts = {'w': 0, 'y': 0, 'g': 0, 'b': 0, 'r': 0, 'o': 0}
def input(key):
    global tiles_index, counts, STATE

    def next():
        global STATE, tiles_index
        if tiles_index < len(all_tiles):
            all_tiles[tiles_index].color = color.cyan
            tiles_index += 1
        else:
            print("Wypełniono wszystko!")
            STATE = 'ROTATE'

    if STATE == 'ROTATE':
        is_shift = held_keys['shift']
        match key:
            case 'r': rotate(0, 1, 90 if is_shift else -90)
            case 'l': rotate(0, -1, 90 if is_shift else -90)
            case 'u': rotate(1, 1, 90 if is_shift else -90)
            case 'd': rotate(1, -1, 90 if is_shift else -90)
            case 'f': rotate(2, 1, 90 if is_shift else -90)
            case 'b': rotate(2, -1, 90 if is_shift else -90)




    elif STATE == 'INPUT_COLORS':
        if key in ('w','y','b','g','r','o'):

            if key == 'w' and counts['w'] < 9:
                all_tiles[tiles_index-1].color = color.white
                counts['w']+=1
                next()
            elif key == 'y' and counts['y'] < 9:
                all_tiles[tiles_index - 1].color = color.yellow
                counts['y']+=1
                next()
            elif key == 'b' and counts['b'] < 9:
                all_tiles[tiles_index - 1].color = color.blue
                counts['b']+=1
                next()
            elif key == 'g' and counts['g'] < 9:
                all_tiles[tiles_index - 1].color = color.green
                counts['g']+=1
                next()
            elif key == 'r' and counts['r'] < 9:
                all_tiles[tiles_index - 1].color = color.red
                counts['r']+=1
                next()
            elif key == 'o' and counts['o'] < 9:
                all_tiles[tiles_index - 1].color = color.orange
                counts['o']+=1
                next()

        elif key == 'l':
            if tiles_index > 1:
                tiles_index-=1
                match all_tiles[tiles_index-1].color:
                    case color.white: counts['w'] -= 1
                    case color.yellow: counts['y'] -= 1
                    case color.blue: counts['b'] -= 1
                    case color.green: counts['g'] -= 1
                    case color.red: counts['r'] -= 1
                    case color.orange:counts['o'] -= 1
                all_tiles[tiles_index].color = color.white
                all_tiles[tiles_index-1].color = color.cyan



app.run()