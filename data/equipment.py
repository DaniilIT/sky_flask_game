from dataclasses import dataclass
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    """ Броня
    """
    name: str
    defence: float
    stamina_per_turn: float

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Weapon:
    """ Оружие
    """
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return round(uniform(self.min_damage, self.max_damage), 1)

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class EquipmentData:
    weapons: list[Weapon]
    armors: list[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        """ Возвращает объект оружия по имени
        """
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon

    def get_armor(self, armor_name) -> Armor:
        """ Возвращает объект брони по имени
        """
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor

    def get_weapons_names(self) -> list:
        """ Возвращаем список с оружием
        """
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        """ Возвращаем список с броней
        """
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        equipment_file = open("./data/equipment.json")
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
