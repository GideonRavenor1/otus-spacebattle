class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @x.setter
    def x(self, value: int) -> None:
        self.__x = value

    @y.setter
    def y(self, value: int) -> None:
        self.__y = value

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other: "Vector") -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    __repr__ = __str__
