TYPE_SHOOTER = 0
TYPE_PREDATOR = 1
TYPE_PREY = 2


capivara = {
    "model": "enemy_capivara",
    "type": TYPE_PREY,
    "attack": 10,  
    "hp": 1,
    "hpRestore": 50
}

onca = {
    "model": "enemy_onca",
    "type": TYPE_PREDATOR,
    "attack": 70,
    "hp": 1,
    "hpRestore": 30
}

indio = {
    "model": "enemy_tupi",
    "type": TYPE_SHOOTER,
    "bullet": "ammo_spear",
    "attack": 50,  
    "hp": 1,
    "hpRestore": 100
}

explorer = {
    "model": "enemy_explorer",
    "type": TYPE_SHOOTER,
    "bullet": "ammo_bullet",
    "attack": 100,  
    "hp": 1,
    "hpRestore": 50,
    "isBoss": True
}

paca = {
    "model": "enemy_paca",
    "type": TYPE_PREY,
    "attack": 5,  
    "hp": 1,
    "hpRestore": 20
}

anta = {
    "model": "enemy_anta",
    "type": TYPE_PREY,
    "attack": 40,  
    "hp": 1,
    "hpRestore": 50
}

jiboia = {
    "model": "enemy_snake",
    "type": TYPE_PREDATOR,
    "attack": 30,  
    "hp": 1,
    "hpRestore": 20
}

piranha = {
    "model": "enemy_piranha",
    "type": TYPE_PREDATOR,
    "attack": 50,  
    "hp": 1,
    "hpRestore": 30
}

jacare = {
    "model": "enemy_jacare",
    "type": TYPE_PREDATOR,
    "attack": 70,  
    "hp": 1,
    "hpRestore": 70
}

land_enemies = [capivara, onca, indio, paca, anta, jiboia]
river_enemies = [piranha, jacare]
all_enemies = land_enemies + river_enemies + [explorer]


def is_human(txt):
    return txt in (indio["model"], explorer["model"])


def get_hp_restore(txt):
    for e in all_enemies:
        if txt == e["model"]:
            return e["hpRestore"]
    return None
