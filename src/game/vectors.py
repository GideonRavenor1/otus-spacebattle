class Vector:
    def __init__(self, x: int, y: int, object_id: str) -> None:
        self.__x = int(x)
        self.__y = int(y)
        self.__object_id = object_id

    @property
    def object_id(self) -> str | None:
        return self.__object_id

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
        return Vector(int(self.x + other.x), int(self.y + other.y), self.object_id)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(int(self.x - other.x), int(self.y - other.y), self.object_id)

    def __eq__(self, other: "Vector") -> bool:
        if self.object_id != other.object_id:
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"Vector({self.x=}, {self.y=}, {self.object_id=})"

    def to_list(self) -> list:
        return [self.x, self.y, self.object_id]

    __repr__ = __str__
