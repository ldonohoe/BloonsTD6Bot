import pyautogui as pag
import pydirectinput as pdi
import logging

import config


class Tower:
    def __init__(self, bot, hotkey, position, upgrade_path, name='tower', target='first'):
        self._name = name
        self._bot = bot
        try:
            self._bot.wait_for(position, tower=True)
        except ValueError as err:
            raise ValueError(f'Error: Could not find {self._name} spot on screen')
        self._position = self._bot.wait_location
        self._hotkey = hotkey
        self._upgrades = [0, 0, 0]
        self._upgrade_path = upgrade_path
        self._target = target
        logging.info('Placing {}'.format(self._name))
        pag.moveTo(self._position)
        while not self._bot._is_present('resources/menu/can_afford_tower.jpg'):
            pdi.press(self._hotkey)
        pag.click()
        if self._target != 'first':
            self._setTarget(self._target)

    def _setTarget(self, target):
        pag.moveTo(self._position)
        pag.click()
        if target == 'strong':
            pdi.press('tab', presses=3)
        elif target == 'close':
            pdi.press('tab', presses=2)
        elif target == 'last':
            pdi.press('tab', presses=1)
        pdi.press('esc')

    @staticmethod
    def _upgrade_track(track):
        pdi.press(config.HOTKEY_UPGRADES[track - 1])

    def _tower_upgrades_to_string(self, track, to_level):
        string = ''
        for i, upgrade_level in enumerate(self._upgrades):
            string += str(to_level) if i + 1 == track else str(upgrade_level)
        return string

    def upgrade(self, track, to_level):
        if track > 3 or to_level > 5:
            logging.error('Track ({}) or level ({}) is too high'.format(track, to_level))
            raise ValueError('Track ({}) or level ({}) is too high'.format(track, to_level))
        pag.click(self._position)
        for i in range(to_level - self._upgrades[track - 1]):
            tower_upgrade_text = self._tower_upgrades_to_string(track, self._upgrades[track - 1] + i + 1)
            logging.info('Waiting for {} {} to become available'.format(self._name, tower_upgrade_text))
            changed = self._bot.wait_for(self._upgrade_path.format(track, self._upgrades[track - 1] + i + 1))
            if changed:
                pag.click(self._position)
            self._upgrade_track(track)
            logging.info('Upgraded {} to {}'.format(self._name, tower_upgrade_text))
        self._upgrades[track - 1] = to_level
        pag.click(self._position)

    def sell(self): 
        pag.click(self._position)
        pdi.press('backspace')
