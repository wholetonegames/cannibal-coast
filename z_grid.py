def make_palette(floor='', z_none='z_none', wall_tile_list=[]):
    return {
        '.': floor,
        '#': wall_tile_list,
        '*': z_none,
        'x': 'exit',
        'e': z_none,
        'n': z_none,
        'b': z_none,
    }


ITEMS = ('b')

palette = {
    'forest': make_palette(wall_tile_list=['grid_forest_wall_1', 'grid_forest_wall_2']),
    'tribe': make_palette(wall_tile_list=['grid_forest_wall_1', 'grid_forest_wall_2']),
    'swamp': make_palette(floor='grid_swamp_floor', z_none='grid_swamp_floor', wall_tile_list=['grid_swamp_wall']),
    'river': make_palette(wall_tile_list=['grid_river_wall_1', 'grid_river_wall_2']),
}
