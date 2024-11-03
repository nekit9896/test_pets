from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Tag:
    id: int
    name: str


@dataclass
class Pet:
    id: int
    category: Category
    name: str
    photoUrls: list[str]
    tags: list[Tag]
    status: str
