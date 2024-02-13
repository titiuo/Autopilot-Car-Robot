import logging


class Position:
    def __init__(self, x: float = 0, y: float = 0, angle: float = 0):
        self.x: float = x
        self.y: float = y
        self.angle: float = angle

    def translate(self, dx: float, dy: float) -> 'Position':
        self.x += dx
        self.y += dy
        return self

    def rotate(self, dangle: float) -> 'Position':
        self.angle += dangle
        return self
    
    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.x+other.x, self.y+other.y, self.angle+other.angle)

    def __mul__(self, other: float) -> 'Position':
        return Position(self.x*other, self.y*other, self.angle*other)
    
    def __truediv__(self, other: float) -> 'Position':
        return Position(self.x/other, self.y/other, self.angle/other)
    
    def __str__(self) -> str:
        return f"x:{self.x},y:{self.y},angle:{self.angle}"

class Robot:
    class Get:
        def __init__(self, id: int):
            if not is_valid_robot_id(id):
                logging.warning(f"Invalid robot id ({id})")
            self.robot_id: int = id
    
    class GetAnswer:
        def __init__(self, id: int, position: Position):
            if not is_valid_robot_id(id):
                logging.warning(f"Invalid robot id ({id})")
            self.robot_id: int = id
            self.position: Position = position

    class Post:
        def __init__(self, id: int, position: Position):
            if not is_valid_robot_id(id):
                logging.warning(f"Invalid robot id ({id})")
            self.robot_id: int = id
            self.position: Position = position


class Marker:
    class Get:
        def __init__(self, id: int):
            if not is_valid_marker_id(id):
                logging.warning(f"Invalid marker id ({id})")
            self.marker_id = id

    class GetAnswer:
        def __init__(self, id: int, position: Position):
            if not is_valid_robot_id(id):
                logging.warning(f"Invalid robot id ({id})")
            self.robot_id: int = id
            self.position: Position = position

    class Post:
        def __init__(self, id: int, position: Position):
            if not is_valid_marker_id(id):
                logging.warning(f"Invalid marker id ({id})")
            self.marker_id: int = id
            self.position: Position = position

class Logic:
    class PostState:
        def __init__(self, state: str):
            self.state: str = state

    class PostMilestone:
        def __init__(self, milestone: str):
            self.milestone: str = milestone


def is_valid_robot_id(id: int):
    return 20 <= id <= 23 or 30 <= id <= 33 or 40 <= id <= 43 or 50 <= id <= 53 or 60 <= id <= 63


def is_valid_marker_id(id: int):
    return 1 <= id <= 5 or id==9 or id==10
