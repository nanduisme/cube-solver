from enum import Enum, auto
from typing import Dict, List

from rich import print


class Move(Enum):
    L = auto()
    R = auto()
    U = auto()
    D = auto()
    B = auto()
    F = auto()

    LP = auto()
    RP = auto()
    UP = auto()
    DP = auto()
    BP = auto()
    FP = auto()


class Color(Enum):
    G = auto()
    R = auto()
    W = auto()
    O = auto()
    Y = auto()
    B = auto()


colors = [Color.W, Color.G, Color.Y, Color.R, Color.O, Color.B]


class Tile:
    def __init__(self, color: Color, num: int):
        self.color = color
        self.num = num


# Rules:
# - WU GF is default position
# - No rotations (for now)


class Cube:
    movement_history: List[Move] = []
    move_color_map = {
        Move.U: Color.W,
        Move.F: Color.G,
        Move.R: Color.R,
        Move.L: Color.O,
        Move.D: Color.Y,
        Move.B: Color.B,
    }
    cube: Dict[Color, List[Tile]] = {
        col: [Tile(col, i) for i in range(0, 9)] for col in colors
    }

    def color_str(self, tile: Tile):
        color = tile.color
        match color:
            case Color.W:
                return "white"
            case Color.Y:
                return "bright_yellow"
            case Color.R:
                return "red"
            case Color.O:
                return "yellow"
            case Color.B:
                return "blue"
            case Color.G:
                return "green"

    def show(self):
        # Yellow side
        c = Color.Y
        for i in [0, 3, 6]:
            print(
                "  " * 3,
                f"[{self.color_str(self.cube[c][i])}]██[{self.color_str(self.cube[c][i + 1])}]██[{self.color_str(self.cube[c][i + 2])}]██",
                "  " * 3,
                sep="",
            )

        # Blue side
        c = Color.B
        for i in [0, 3, 6]:
            print(
                "  " * 3,
                f"[{self.color_str(self.cube[c][i])}]██[{self.color_str(self.cube[c][i + 1])}]██[{self.color_str(self.cube[c][i + 2])}]██",
                "  " * 3,
                sep="",
            )

        # OWR 1
        bor = [Color.O, Color.W, Color.R]
        for i in [0, 3, 6]:
            for c in bor:
                print(
                    f"[{self.color_str(self.cube[c][i])}]██[{self.color_str(self.cube[c][i + 1])}]██[{self.color_str(self.cube[c][i + 2])}]██",
                    end="",
                )
            print("")

        # Green side
        c = Color.G
        for i in [0, 3, 6]:
            print(
                "  " * 3,
                f"[{self.color_str(self.cube[c][i])}]██[{self.color_str(self.cube[c][i + 1])}]██[{self.color_str(self.cube[c][i + 2])}]██",
                "  " * 3,
                sep="",
            )

    def moves(self, *moves: Move):
        for m in moves:
            self.move(m)

    def rotate_face(self, move: Move):
        c = self.move_color_map[move]
        rotation_map = {
            0: 6,
            1: 3,
            2: 0,
            3: 7,
            4: 4,
            5: 1,
            6: 8,
            7: 5,
            8: 2,
        }

        temp_side = [Tile(Color.W, 0) for _ in range(9)]
        for dest, origin in rotation_map.items():
            temp_side[dest] = self.cube[c][origin]

        self.cube[c] = temp_side

    def move(self, move: Move):
        self.movement_history.append(move)
        match move:
            case Move.L:
                self.rotate_face(move)
                for i in [0, 3, 6]:
                    (
                        self.cube[Color.G][i],
                        self.cube[Color.W][i],
                        self.cube[Color.B][i],
                        self.cube[Color.Y][i],
                    ) = (
                        self.cube[Color.W][i],
                        self.cube[Color.B][i],
                        self.cube[Color.Y][i],
                        self.cube[Color.G][i],
                    )

            case Move.LP:
                for _ in range(3):
                    self.move(Move.L)

            case Move.R:
                self.rotate_face(move)
                for i in [2, 5, 8]:
                    (
                        self.cube[Color.W][i],
                        self.cube[Color.B][i],
                        self.cube[Color.Y][i],
                        self.cube[Color.G][i],
                    ) = (
                        self.cube[Color.G][i],
                        self.cube[Color.W][i],
                        self.cube[Color.B][i],
                        self.cube[Color.Y][i],
                    )

            case Move.RP:
                for _ in range(3):
                    self.move(Move.R)

            case Move.F:
                self.rotate_face(move)
                for i in [6, 7, 8]:
                    # TODO: fix for orange
                    (
                        self.cube[Color.R][i],
                        self.cube[Color.Y][i - 6],
                        self.cube[Color.O][i],
                        self.cube[Color.W][i],
                    ) = (
                        self.cube[Color.W][i],
                        self.cube[Color.R][i],
                        self.cube[Color.Y][i - 6],
                        self.cube[Color.O][i],
                    )

            case Move.FP:
                for _ in range(3):
                    self.move(Move.F)


cube = Cube()

while True:
    m = input("Enter your move: ").lower()
    match m:
        case "l":
            cube.move(Move.L)
        case "lp":
            cube.move(Move.LP)
        case "r":
            cube.move(Move.R)
        case "rp":
            cube.move(Move.RP)
        case "f":
            cube.move(Move.F)
        case "fp":
            cube.move(Move.FP)
        case ".":
            break
    cube.show()
