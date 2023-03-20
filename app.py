from flask import Flask, render_template, request, redirect, url_for, abort

from data.base import Arena
from data.classes import unit_classes
from data.equipment import Equipment
from data.unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {}
arena = Arena()
equipment = Equipment()


@app.route('/')
def menu_page():
    """ Главное меню
    """
    return render_template('index.html')


@app.route('/fight/')
def start_fight():
    """ Экран боя
    """
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes, result='Бой начался!')


@app.route('/fight/hit')
def hit():
    """ Нанесение удара
    """
    if arena.game_is_running:
        result = arena.player_hit()
        battle_result = arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)
    abort(400)


@app.route('/fight/use-skill')
def use_skill():
    """ Использование скилла
    """
    if arena.game_is_running:
        if result := arena.player_use_skill():
            battle_result = arena.next_turn()
        else:
            result = 'Навык использован'
            battle_result = ''
        return render_template('fight.html', heroes=heroes, result=result, battle_result=battle_result)
    abort(400)


@app.route('/fight/pass-turn')
def pass_turn():
    """ Пропуск хода
    """
    battle_result = arena.next_turn()
    return render_template('fight.html', heroes=heroes, battle_result=battle_result)


@app.route('/fight/end-fight')
def end_fight():
    """ Завершение игры
    """
    arena._end_game()
    return redirect(url_for('menu_page')), 302


@app.route('/choose-hero/', methods=['GET', 'POST'])
def choose_hero():
    """ Выбор героя
    """
    if request.method == 'GET':
        return render_template('hero_choosing.html',
                               result={
                                   'header': 'Выберите героя',
                                   'classes': unit_classes,
                                   'weapons': equipment.get_weapons_names(),
                                   'armors': equipment.get_armors_names(),
                               })
    elif request.method == 'POST':
        unit_class = request.form.get('unit_class')
        player = PlayerUnit(name=request.form.get('name'),
                            unit_class=unit_classes.get(unit_class))

        weapon_name = request.form.get('weapon')
        player.equip_weapon(equipment.get_weapon(weapon_name))

        armor_name = request.form.get('armor')
        player.equip_armor(equipment.get_armor(armor_name))

        heroes['player'] = player
        return redirect(url_for('choose_enemy')), 302


@app.route('/choose-enemy/', methods=['GET', 'POST'])
def choose_enemy():
    """ Выбор врага
    """
    if request.method == 'GET':
        return render_template('hero_choosing.html',
                               result={
                                   'header': 'Выберите врага',
                                   'classes': unit_classes,
                                   'weapons': equipment.get_weapons_names(),
                                   'armors': equipment.get_armors_names(),
                               })
    if request.method == 'POST':
        unit_class = request.form.get('unit_class')
        enemy = EnemyUnit(name=request.form.get('name'),
                          unit_class=unit_classes.get(unit_class))

        weapon_name = request.form.get('weapon')
        enemy.equip_weapon(Equipment().get_weapon(weapon_name))

        armor_name = request.form.get('armor')
        enemy.equip_armor(Equipment().get_armor(armor_name))

        heroes['enemy'] = enemy
        return redirect(url_for('start_fight')), 302
