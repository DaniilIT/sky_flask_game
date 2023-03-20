class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def start_game(self, player, enemy):
        """ Начать игру
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        """ Проверка здоровья игроков
        """
        if self.player.health_points <= 0 and self.enemy.health_points <= 0:
            return 'Никто не устоял в бою! Ничья!'
        if self.player.health_points <= 0:
            return 'Не могу поверить, Вы проиграли!'
        if self.enemy.health_points <= 0:
            return 'Битва отгремела не напрасно! Вы победили!'
        return None

    def _stamina_regeneration(self):
        """ Регенерация выносливости
        """
        self.player.stamina += self.STAMINA_PER_ROUND
        if self.player.stamina > self.player.unit_class.max_stamina:
            self.player.stamina = self.player.unit_class.max_stamina

        self.enemy.stamina += self.STAMINA_PER_ROUND
        if self.enemy.stamina > self.enemy.unit_class.max_stamina:
            self.enemy.stamina = self.enemy.unit_class.max_stamina

    def next_turn(self):
        """ Следующий ход
        """
        # проверка, осталось ли еще здоровье у игроков.
        if self._check_players_hp():
            return self._end_game()
        self._stamina_regeneration()
        return self.enemy.hit(self.player)

    def _end_game(self):
        """ Конец игры
        """
        self._instances = {}
        self.game_is_running = False
        return self._check_players_hp()

    def player_hit(self):
        """ Удар игрока
        """
        self._stamina_regeneration()
        return self.player.hit(self.enemy)

    def player_use_skill(self):
        """ Использование умения игрока
        """
        self._stamina_regeneration()
        return self.player.use_skill(self.enemy)
