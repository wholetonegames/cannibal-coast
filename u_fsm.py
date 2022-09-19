import random
from w_menu_start import StartMenu
from w_board_enemy import BoardEnemy
from w_board_npc import BoardNPC
from u_imports import ConfigImports
from u_controls import ConfigControls
from w_menu_config import ConfigMenu
from w_game_over import GameOverScreen
from w_cutscene import Cutscene
from direct.fsm.FSM import FSM
import z_m


class ConfigFSM(FSM, ConfigImports, ConfigControls):
    def __init__(self):
        self.gridStage = None
        FSM.__init__(self, "FSM-Game")
        ConfigImports.__init__(self)
        ConfigControls.__init__(self)
        self.defaultTransitions = {
            'StartMenu': ['GameLoop', 'Cutscene'],
            'GameLoop': ['PauseMenu', 'GameOver'],
            'PauseMenu': ['StartMenu', 'GameLoop'],
            'GameOver': ['StartMenu', 'GameLoop', 'Cutscene'],
            'Cutscene': ['GameLoop', 'StartMenu']
        }

    # FSM ##################################################################

    def enterStartMenu(self):
        base.removeLoadingScreen()
        self.initController()
        self.startMenu = StartMenu()

        if self.gridStage:
            self.gridStage.quit()

        self.accept(z_m.MENU_START, self.startNewGame)
        self.accept(z_m.MENU_LOAD, self.loadGame)
        self.accept(z_m.MENU_QUIT, self.userExit)

        taskMgr.add(self.startMenu.readKeys, "readKeysTask")
        base.messenger.send("playBGM")

    def exitStartMenu(self):
        self.resetButtons()
        self.ignore(z_m.MENU_START)
        self.ignore(z_m.MENU_LOAD)
        self.ignore(z_m.MENU_QUIT)

        taskMgr.remove("readKeysTask")
        self.startMenu.quit()
        del self.startMenu

    def enterGameLoop(self):
        self.initController()
        base.removeLoadingScreen()
        if not self.gridStage:
            self.choose_board()
        self.accept(z_m.MENU_PAUSE, self.request, ['PauseMenu'])
        self.accept(z_m.MENU_GAMEOVER, self.request, ['GameOver'])
        self.accept(z_m.CALL_BOARD, self.gridStage.requestBoardChange)
        self.accept(z_m.STATUS_BULLETS, self.gameData.set_item,
                    [self.gameData.STATUS_BULLETS])
        self.accept(z_m.CHANGE_NAME, self.change_player_name)
        self.accept(z_m.GRUNT_KILLED, self.grunt_killed)
        self.accept(z_m.PLAYER_HURT, self.player_hurt)
        self.accept(z_m.GOT_ITEM, self.got_item)
        self.accept(z_m.REFRESH_HUD, self.refresh_hud)
        self.accept(z_m.BOSS_KILLED, self.boss_killed)

        self.gridStage.start()
        self.initController()

    def exitGameLoop(self):
        self.resetButtons()
        self.ignore(z_m.MENU_PAUSE)
        self.ignore(z_m.MENU_GAMEOVER)
        self.ignore(z_m.CALL_BOARD)
        self.ignore(z_m.CHANGE_NAME)
        self.ignore(z_m.GRUNT_KILLED)
        self.ignore(z_m.PLAYER_HURT)
        self.ignore(z_m.GOT_ITEM)
        self.ignore(z_m.STATUS_BULLETS)
        self.ignore(z_m.REFRESH_HUD)
        self.ignore(z_m.BOSS_KILLED)
        self.gridStage.stop()

    def enterPauseMenu(self):
        self.initController()
        self.configMenu = ConfigMenu()
        self.accept(z_m.CHARA_ADD, self.configMenu.change_config, [1])
        self.accept(z_m.CHARA_SUB, self.configMenu.change_config, [-1])
        self.accept(z_m.BACK_GAME, self.request, ['GameLoop'])
        self.accept(z_m.BACK_START, self.request, ['StartMenu'])
        taskMgr.add(self.configMenu.readKeys, "readKeysTask")

    def exitPauseMenu(self):
        self.resetButtons()
        self.ignore(z_m.CHARA_ADD)
        self.ignore(z_m.CHARA_SUB)
        self.ignore(z_m.BACK_GAME)
        self.ignore(z_m.BACK_START)
        taskMgr.remove("readKeysTask")
        self.configMenu.quit()
        del self.configMenu

    def enterGameOver(self):
        base.removeLoadingScreen()
        self.initController()
        self.accept(z_m.BACK_START, self.request, ['StartMenu'])
        self.accept(z_m.BACK_CUTSCENE, self.request, ['Cutscene'])
        self.accept(z_m.BACK_GAME, self.request, ['GameLoop'])
        self.accept(z_m.CHANGE_BOARD_HP, self.change_board_hp)
        self.accept(z_m.SAVE_GAME, self.saveGame)
        self.game_over = GameOverScreen(
            self.gridStage.player.is_ko, self.is_last_stage, self.is_save_stage)

    def exitGameOver(self):
        self.resetButtons()
        self.ignore(z_m.BACK_START)
        self.ignore(z_m.BACK_CUTSCENE)
        self.ignore(z_m.BACK_GAME)
        self.ignore(z_m.SAVE_GAME)
        self.ignore(z_m.CHANGE_BOARD_HP)
        self.game_over.quit()
        del self.game_over

    def enterCutscene(self):
        self.initController()
        txt, img = self.getCutsceneText()
        self.cutScene = Cutscene(txt, img)
        taskMgr.add(self.cutScene.readKeys, "readKeysTask")
        self.accept(z_m.PLAY_CANCEL, self.afterCutscene)

    def exitCutscene(self):
        self.resetButtons()
        self.cutScene.quit()
        taskMgr.remove("readKeysTask")
        del self.cutScene

    # FSM ##################################################################
    def boss_killed(self):
        self.gameData.increment_boss_killed_count()

    def afterCutscene(self):
        if self.is_last_stage:
            self.request('StartMenu')
        else:
            self.request('GameLoop')

    def getCutsceneText(self):
        txt = ''
        img= ''
        if self.is_last_stage:
            if self.gameData.isCannibal:
                if self.gameData.has_killed_every_boss:
                    txt = '''
                    At the last second, you decide not to go back to Europe.
                    A place where no one would comprehend the circumstances that forced you to
                    become a cannibal.

                    Whereas in Brazil, the Tupinambá would welcome your cannibalism with open arms.
                    Armed with your knowledge of the Tupi language, you head back to the jungle.

                    A place where might makes right. Where he who eats not... Gets eaten!

                    The End.
                    '''
                    img = 'caramuru.png'
                else:
                    txt = ''' 
                    At long last, you board a ship to Europe.
                    But the sailors soon figure out that you have consumed human flesh.

                    Fearing for their own safety, they throw you overboard so that the
                    sharks can do to you the same you did to your fellow men.

                    The End.     
                    '''
                    img = 'sailors.png'
            else:
                txt = '''
                At long last, you board a ship to Europe.
                You try your best to forget all the horrors you have seen in the Tropics.

                Try as you may, the memories don't leave your mind, so you decide to
                write down your misadventures in what others would call "ElDorado".

                The End.
                '''
                img = 'book.png'
        else:
            txt = '''
            The year is 1509. You have been shipwrecked off the coast of Brazil.
            You have been betrayed by your crew members and handed to the cannibalistic Tupinambá natives.
        
            You have freed yourself and now you must find a way to head back to Europe.
            Will you get revenge on your crew, head back to civilisation
            Or will you succumb to the wicked ways of the Cannibal Coast?
            '''
            img = 'brazil_map.png'
        txt += "\n...Press Cancel to Continue..."
        return [txt, img]

    def startNewGame(self):
        self.gameData.resetGameModel()
        self.choose_board()
        self.request('Cutscene')

    def loadGame(self):
        try:
            self.gameData.loadGame()
        except:
            # if nothing to load, just start a new game
            self.gameData.resetGameModel()
        self.choose_board()
        self.request('GameLoop')

    def saveGame(self):
        self.gameData.saveGame()

    def choose_board(self):
        try:
            self.gridStage.quit()
        except:
            pass
        finally:
            del self.gridStage
        self.gridStage = None
        index = self.gameData.current_board_index
        self.set_map(index)

    def set_map(self, index):
        if self.is_enemy_board:
            self.gridStage = BoardEnemy()
        else:
            self.gridStage = BoardNPC()

    @property
    def is_enemy_board(self):
        return 'enemyNumber' in self.mapData.maps[self.gameData.current_board_index]

    def next_map(self):
        self.gameData.increment_board(len(self.mapData.maps))
        self.choose_board()

    def change_player_name(self, name):
        self.gameData.change_player_name(name)

    def grunt_killed(self, pos, index):
        self.gridStage.add_enemy_item(pos, index)

    def player_hurt(self):
        self.gameData.set_lives(self.gridStage.player.hp)

    def refresh_hud(self):
        self.gridStage.hud.set_lives()
        self.gridStage.hud.set_ammo()

    def got_item(self, item):
        self.gameData.set_item(item)

    def change_board_hp(self):
        self.gameData.change_board_hp()

    @property
    def is_last_stage(self):
        return self.gameData.current_board_index == self.mapData.last_index

    @property
    def is_save_stage(self):
        return self.gameData.current_board_index != 0 and self.gameData.current_board_index % 6 == 0
