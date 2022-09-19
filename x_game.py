from i_save_load import SaveLoadJSON
import z_enemy
import y_helpers
import os
import z_m
import math


class GameModel(SaveLoadJSON):
    STATUS_BULLETS = 'b'
    STARTER_NAME = 'Diogo Álvares'
    STATUS_MAX_NUMBER = 1
    FULL_HEALTH_NORMAL = 100
    FULL_HEALTH_CANNIBAL = 200

    def __init__(self, saveFolderPath):
        SaveLoadJSON.__init__(self, saveFolderPath)
        self.saveSlotNumbers = (1, 2, 3)
        self.protectedFields.append('saveSlotNumbers')
        self.selectedSaveSlot = 1
        self.protectedFields.append('selectedSaveSlot')
        # at the end, always
        self.resetGameModel()

    def getSaveFileInfo(self, filename):
        json_data = self.get_text(filename)
        totalTime = 0
        thisMap = 'Nowhere'
        if 'current_board_index' in json_data:
            thisMap = json_data['current_board_index']
        if 'totalTimePlayed' in json_data:
            totalTime = y_helpers.pretty_print_time(
                json_data['totalTimePlayed'])
        return (thisMap, totalTime)

    def runManualUpdates(self):
        self.filepath = os.path.dirname(self.filepath) + \
            "/slot{}.txt".format(self.selectedSaveSlot)
        self.totalTimePlayed += (base.elapsedSeconds - self.previousSavedTime)
        self.previousSavedTime = base.elapsedSeconds

    def resetGameModel(self):
        self.previousSavedTime = 0
        self.player_name = self.STARTER_NAME
        self.heroHP = self.FULL_HEALTH_NORMAL
        self.bullet_timer = 3.0  # bullet can fly as long as it needs to
        self.ammo = 0
        self.status_cannibal = 0
        self.current_board_index = 0
        self.boss_killed_count = 0
        self.totalTimePlayed = 0
        self.sfx_vol = 1
        self.bgm_vol = 1

    def increment_board(self, arr_len):
        self.current_board_index += 1

    def change_player_name(self, name):
        self.player_name = name

    @property
    def isCannibal(self):
        return self.status_cannibal > 0

    @property
    def has_killed_every_boss(self):
        return self.boss_killed_count == y_helpers.MAX_STAGE_LOOP

    def increment_boss_killed_count(self):
        self.boss_killed_count += 1

    def set_lives(self, heroHP):
        self.heroHP = heroHP
        base.messenger.send(z_m.REFRESH_HUD)

    def add_lives(self, heroHP):
        if self.isCannibal:
            heroHP = math.ceil(heroHP / 2)
        self.heroHP += heroHP
        self.heroHP = max(self.heroHP, 0)
        # if not a cannibal, health clamps at 100%
        if self.isCannibal:
            self.heroHP = min(self.heroHP, self.FULL_HEALTH_CANNIBAL)
        else:
            self.heroHP = min(self.heroHP, self.FULL_HEALTH_NORMAL)
        base.messenger.send(z_m.REFRESH_HUD)

    def add_bullets(self, ammo):
        self.ammo += ammo
        base.messenger.send(z_m.REFRESH_HUD)

    @property
    def enemy_level(self):
        return (self.current_board_index // 10) + 1

    def set_item(self, txt):
        if txt == self.STATUS_BULLETS:
            self.add_bullets(3)
            base.messenger.send(z_m.REFRESH_HUD)
            return

        if z_enemy.is_human(txt):
            self.status_cannibal = 1
            if self.player_name == self.STARTER_NAME:
                self.change_player_name('Caramuru')
                base.messenger.send("sfxScream")

        hp_restore = z_enemy.get_hp_restore(txt)
        if hp_restore:
            self.add_lives(hp_restore)
        base.messenger.send(z_m.REFRESH_HUD)

    def change_board_hp(self):
        decrement = 10
        if self.heroHP > decrement:
            self.heroHP -= decrement
