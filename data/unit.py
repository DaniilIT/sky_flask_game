from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint

from data.classes import UnitClass
from data.equipment import Weapon, Armor


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """ При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return self.hp

    @property
    def stamina_points(self):
        return self.stamina

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f'{self.name} экипирован оружием {self.weapon.name}'

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f'{self.name} экипирован броней {self.weapon.name}'

    def _count_damage(self, target: BaseUnit) -> int:
        # расчет урона
        damage = round(self.weapon.damage * self.unit_class.attack, 1)

        #  расчет брони
        defence_cost = round(target.armor.stamina_per_turn * target.unit_class.stamina, 1)
        if target.stamina >= defence_cost:
            # уменьшение выносливости защищающегося
            target.stamina = round(target.stamina - defence_cost, 1)

            amount_defence = round(target.armor.defence * target.unit_class.armor, 1)
            damage = round(damage - amount_defence, 1)
            if damage < 0:
                damage = 0

        # уменьшение выносливости атакующего при ударе
        amount_stamina = round(self.weapon.stamina_per_hit * self.unit_class.stamina, 1)
        self.stamina = round(self.stamina - amount_stamina, 1)

        # нанесение урона
        target.get_damage(damage)

        return damage

    def get_damage(self, damage: float) -> None:
        """ Получение урона
        """
        self.hp = round(self.hp - damage, 1)
        if self.hp < 0:
            self.hp = 0

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:
        if self._is_skill_used:
            return None

        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.stamina_points >= round(self.weapon.stamina_per_hit * self.unit_class.stamina, 1):
            damage = self._count_damage(target)
            if damage:
                return f'{self.name} используя {self.weapon.name} ' \
                       f'пробивает {target.armor.name} соперника и наносит {damage} урона.'
            return f'{self.name} используя {self.weapon.name} ' \
                   f'наносит удар, но {target.armor.name} соперника его останавливает.'
        return f'{self.name} попытался использовать {self.weapon.name} ' \
               f', но у него не хватило выносливости.'


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if randint(1, 10) == 10 and not self._is_skill_used:
            return self.use_skill(target)

        if self.stamina >= round(self.weapon.stamina_per_hit * self.unit_class.stamina, 1):
            damage = self._count_damage(target)
            if damage:
                return f'{self.name} используя {self.weapon.name} ' \
                       f'пробивает {target.armor.name} и наносит Вам {damage} урона.'
            return f'{self.name} используя {self.weapon.name} ' \
                   f'наносит удар, но Ваш(а) {target.armor.name} его останавливает.'
        return f'{self.name} попытался использовать {self.weapon.name} ' \
               f', но у него не хватило выносливости.'
