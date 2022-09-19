class ConfigSound:
    def __init__(self):
        self.music = None
        self.sound = None
        self.sfxEnemyHurt = base.loader.loadSfx("sfx_enemy_hurt.wav")
        self.sfxHeroHurt = base.loader.loadSfx("sfx_hero_hurt.wav")
        self.sfxHeroShoot = base.loader.loadSfx("sfx_hero_shoot.wav")
        self.sfxItem = base.loader.loadSfx("sfx_item.wav")
        self.sfxBullet = base.loader.loadSfx("sfx_bullet.wav")
        self.sfxScream = base.loader.loadSfx("sfx_scream.wav")
        self.bgmIntro = base.loader.loadMusic("bgm_cannibal.ogg")

        base.accept("sfxEnemyHurt", self.play_sound, [self.sfxEnemyHurt])
        base.accept("sfxHeroHurt", self.play_sound, [self.sfxHeroHurt])
        base.accept("sfxHeroShoot", self.play_sound, [self.sfxHeroShoot])
        base.accept("sfxItem", self.play_sound, [self.sfxItem])
        base.accept("sfxBullet", self.play_sound, [self.sfxBullet])
        base.accept("sfxScream", self.play_sound, [self.sfxScream])

        base.accept("playBGM", self.playMusic)
        base.accept("BGMvolume", self.set_bgm_volume)
        base.accept("SFXvolume", self.set_sfx_volume)

    def playMusic(self):
        if self.music:
            return
        self.music = self.bgmIntro
        self.music.setVolume(base.gameData.bgm_vol)
        self.music.setLoop(True)
        self.music.play()

    def play_sound(self, sound):
        self.sound = sound
        self.sound.setVolume(base.gameData.sfx_vol)
        self.sound.play()

    def set_sfx_volume(self):
        self.music.setVolume(base.gameData.bgm_vol)

    def set_bgm_volume(self):
        self.music.setVolume(base.gameData.bgm_vol)
