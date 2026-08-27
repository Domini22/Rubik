from ursina import *
from dicts import COLOR_TO_CHAR, CHAR_TO_COLOR, cube_state, EDGES, layers, face_order, counts, info_text, MOVE_AXIS_LAYER, CAMERA_ROTATIONS, STICKER_CONFIG, STICKER_CONFIG_2
from enums import AppState
from solver import find_white_edges

app = Ursina()

ec = EditorCamera()
ec.move_speed = 0


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

            for cond, face, pos, rot, col in STICKER_CONFIG: #STICKER_CONFIG_2
                if cond(x,y,z):
                    c = Entity(parent=cubie, model='quad', color=col, position=pos, rotation=rot, scale=0.88)
                    layers[face].append(c)

layers['F'].sort(key=lambda t: (-t.parent.y, -t.parent.x))
layers['B'].sort(key=lambda t: (-t.parent.y, t.parent.x))

layers['L'].sort(key=lambda t: (-t.parent.y, -t.parent.z))
layers['R'].sort(key=lambda t: (-t.parent.y, t.parent.z))

layers['U'].sort(key=lambda t: (-t.parent.z, -t.parent.x))
layers['D'].sort(key=lambda t: (t.parent.z, -t.parent.x))

STATE = AppState.INPUT_COLORS #ROTATE
all_tiles = []
tiles_index = 1
if STATE == AppState.INPUT_COLORS:
    for face in face_order:
        all_tiles.extend(layers[face])
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

def next_tile():
    global STATE, tiles_index
    if tiles_index % 9 == 0:
        face_index = tiles_index // 9
        if face_index in CAMERA_ROTATIONS:
            ec.animate_rotation(CAMERA_ROTATIONS[face_index], duration=1, curve=curve.out_quad)

    if tiles_index < len(all_tiles):
        all_tiles[tiles_index].color = color.cyan
        tiles_index += 1
    else:
        info_text.text = "Wypełniono wszystko!\n[R] - Układaj sam\n[G] - Pokaż instrukcje"
        print(cube_state)
        STATE = AppState.CHOOSE_MODE

def input(key):
    global tiles_index, STATE


    if STATE == AppState.CHOOSE_MODE:
        if key == 'r':
            info_text.text = "Tryb ręczny (Shift = ruch odwrotny)"
            STATE = AppState.ROTATE
        elif key == 'g':
            info_text.text = "Tryb instrukcji:\nKrok 1: Układanie białego krzyża"
            STATE = AppState.GUIDE


    elif STATE == AppState.ROTATE:
        if key in MOVE_AXIS_LAYER:
            axis, layer = MOVE_AXIS_LAYER[key]
            angle = 90 if held_keys['shift'] else -90
            rotate(axis,layer, angle)




    elif STATE == AppState.INPUT_COLORS:
        if key in counts and counts[key] < 9:
            current_face = face_order[(tiles_index - 1) // 9]
            current_slot = (tiles_index - 1) % 9
            all_tiles[tiles_index-1].color = CHAR_TO_COLOR[key]
            cube_state[current_face][current_slot] = key
            counts[key] +=1
            next_tile()

        elif key == 'l' and tiles_index > 1:
            tiles_index-=1
            current_face = face_order[(tiles_index - 1) // 9]
            current_slot = (tiles_index - 1) % 9
            prev_char = cube_state[current_face][current_slot]
            if prev_char in counts: counts[prev_char]-=1
            cube_state[current_face][current_slot] = None
            all_tiles[tiles_index].color = color.white
            all_tiles[tiles_index-1].color = color.cyan



app.run()