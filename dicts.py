from ursina import color, Text

COLOR_TO_CHAR = {
    color.white: 'w',
    color.yellow: 'y',
    color.green: 'g',
    color.blue: 'b',
    color.red: 'r',
    color.orange: 'o'
}

CHAR_TO_COLOR = {
    'w': color.white,
    'y': color.yellow,
    'g': color.green,
    'b': color.blue,
    'r': color.red,
    'o': color.orange
}

STICKER_CONFIG = [
    (lambda x, y, z: y ==  1, 'U', (0,  0.501, 0), (90, 0, 0),
     lambda x, y, z: color.white if (x == 0 and z == 0) else color.gray),
    (lambda x, y, z: y == -1, 'D', (0, -0.501, 0), (270, 0, 0),
     lambda x, y, z: color.yellow if (x == 0 and z == 0) else color.gray),
    (lambda x, y, z: x ==  1, 'R', (0.501, 0, 0), (0, 270, 0),
     lambda x, y, z: color.red if (y == 0 and z == 0) else color.gray),
    (lambda x, y, z: x == -1, 'L', (-0.501, 0, 0), (0, 90, 0),
     lambda x, y, z: color.orange if (y == 0 and z == 0) else color.gray),
    (lambda x, y, z: z ==  1, 'B', (0, 0, 0.501), (0, 180, 0),
     lambda x, y, z: color.blue if (x == 0 and y == 0) else color.gray),
    (lambda x, y, z: z == -1, 'F', (0, 0, -0.501), (0, 0, 0),
     lambda x, y, z: color.green if (x == 0 and y == 0) else color.gray),
]
STICKER_CONFIG_2 = [
    (lambda x, y, z: y ==  1, 'U', (0,  0.501, 0), (90, 0, 0), color.white),
    (lambda x, y, z: y == -1, 'D', (0, -0.501, 0), (270, 0, 0), color.yellow),
    (lambda x, y, z: x ==  1, 'R', (0.501, 0, 0), (0, 270, 0), color.red),
    (lambda x, y, z: x == -1, 'L', (-0.501, 0, 0), (0, 90, 0), color.orange),
    (lambda x, y, z: z ==  1, 'B', (0, 0, 0.501), (0, 180, 0), color.blue),
    (lambda x, y, z: z == -1, 'F', (0, 0, -0.501), (0, 0, 0), color.green),
]

cube_state = {
    'U': ['w'] * 9,
    'D': ['y'] * 9,
    'F': ['g'] * 9,
    'B': ['b'] * 9,
    'R': ['r'] * 9,
    'L': ['o'] * 9,
}

EDGES = [
    # Górna warstwa (U)
    (('U', 1), ('B', 1)),  # U-B
    (('U', 3), ('L', 1)),  # U-L
    (('U', 5), ('R', 1)),  # U-R
    (('U', 7), ('F', 1)),  # U-F

    # Warstwa środkowa (boki)
    (('F', 3), ('L', 5)),  # F-L
    (('F', 5), ('R', 3)),  # F-R
    (('B', 3), ('R', 5)),  # B-R
    (('B', 5), ('L', 3)),  # B-L

    # Dolna warstwa (D)
    (('D', 1), ('F', 7)),  # D-F
    (('D', 3), ('L', 7)),  # D-L
    (('D', 5), ('R', 7)),  # D-R
    (('D', 7), ('B', 7)),  # D-B
]

CORNERS = [
    # Górna warstwa (U)
    (('U', 0), ('B', 2), ('L', 0)),  # U-B-L
    (('U', 2), ('B', 0), ('R', 2)),  # U-B-R
    (('U', 6), ('F', 0), ('L', 2)),  # U-F-L
    (('U', 8), ('F', 2), ('R', 0)),  # U-F-R

    # Dolna warstwa (D)
    (('D', 0), ('F', 6), ('L', 8)),  # D-F-L
    (('D', 2), ('F', 8), ('R', 6)),  # D-F-R
    (('D', 6), ('B', 8), ('L', 6)),  # D-B-L
    (('D', 8), ('B', 6), ('R', 8)),  # D-B-R
]

CENTER_COLORS = {
    'U': 'w',  # Góra - Biały
    'D': 'y',  # Dół - Żółty
    'F': 'g',  # Przód - Zielony
    'B': 'b',  # Tył - Niebieski
    'R': 'r',   # Prawo - Czerwony
    'L': 'o',  # Lewo - Pomarańczowy
}

layers={'U': [], 'D':[], 'R': [], 'L': [], 'F': [], 'B': []}

face_order = ['F', 'L', 'B', 'R', 'U', 'D']

counts = {'w': 0, 'y': 0, 'g': 0, 'b': 0, 'r': 0, 'o': 0}

MOVE_AXIS_LAYER = {
    'r': (0,  1), 'l': (0, -1),
    'u': (1,  1), 'd': (1, -1),
    'b': (2,  1), 'f': (2, -1)
}

CAMERA_ROTATIONS = {
    1: (0, 90, 0),
    2: (0, 180, 0),
    3: (0, 270, 0),
    4: (90, 270, 0),
    5: (-90, 270, 0)
}

info_text = Text(
    text='Wprowadź kolory ścianek',
    origin=(0, 0),
    position=(0, 0.4),
    scale=1.3,
    color=color.yellow
)