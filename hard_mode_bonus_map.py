import logging
import map
import config
from bot import Bot
from tower import Tower



class HardModeBonusMap(Bot):

    def __init__(self):
        super().__init__()
        self._map = map.HardModeBonusMap()

    def _load_game(self):
        if config.DO_OPEN_MONKEYS or self._game_counter == 1:
            newMap = self._map.findNextMap()
            logging.info(f'Found next bonus map: {self._map._name}')
        else:
            self._load_next_game_trick()

    def _load_next_game_trick(self):
        self.click_on(config.BUTTON_GAME_FREEPLAY)
        pdi.press('esc')
        pdi.press('esc')
        self.click_on(config.BUTTON_GAME_TO_HOME)
        newMap = self._map.findNextMap()

    # Single game
    def _play_game(self):
        self._load_game()
        self._wait_for_map_load()

        configDir = config.BEGINNER_MAP_FILES.format(self._map._name)

        hero = Tower(self, config.HOTKEY_HERO, f'{configDir}/hero.jpg', None, 'hero')

        logging.info('Starting game')
        self._start_game()

        dart = Tower(self, config.HOTKEY_TOWER_DART, f'{configDir}/dart.jpg',
                      config.TOWER_DART_UPGRADE, 'dart')
        dart.upgrade(2, 2)
        dart.upgrade(3, 4)

        wizard = Tower(self, config.HOTKEY_TOWER_WIZARD, f'{configDir}/wizard.jpg',
                             config.TOWER_WIZARD_UPGRADE, 'wizard')
        wizard.upgrade(2, 2)
        wizard.upgrade(3, 5)
        dart.upgrade(3, 5)

        self._wait_for_game_completion()
        self._game_completed()


if __name__ == '__main__':
    bot = HardModeBonusMap()
    bot.main()
