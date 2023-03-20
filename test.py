from dataclasses import dataclass

@dataclass
class UnitClass:
    name: str
    max_health: float

WarriorClass = UnitClass(
    name='Воин',
    max_health=60.0,
)


