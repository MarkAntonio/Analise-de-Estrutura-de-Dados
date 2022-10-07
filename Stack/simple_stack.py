from __future__ import annotations
from typing import List, Any
from copy import deepcopy


class Stack:
    def __init__(self) -> None:
        self.__data: List[Any] = []
        self.__index = 0

    def push(self, data: Any) -> None:
        self.__data.append(data)

    def pop(self) -> Any:
        return self.__data.pop()

    def __repr__(self):
        return f'{self.__class__.__name__}{self.__data}'

    def __iter__(self) -> Stack:
        self.__index = len(self.__data)
        return self
    def __next__(self) -> Any:
        if self.__index == 0:
            raise StopIteration
        self.__index -= 1
        return self.__data[self.__index]

    def __bool__(self) -> bool:
        return bool(self.__data)
