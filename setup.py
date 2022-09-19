from setuptools import setup

setup(
    name="cannibal_coast",
    options={
        'build_apps': {
            'platforms': [
                'win_amd64',
            ],
            'include_patterns': [
                '**/*.mf',
            ],
            'exclude_patterns': [
                '**/*.ogg',
                '**/*.wav',
                '**/*.txt',
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.bam'
            ],
            'gui_apps': {
                'cannibal_coast': 'game.py',
            },
            'log_filename': 'output.log',
            'log_append': True,
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)
