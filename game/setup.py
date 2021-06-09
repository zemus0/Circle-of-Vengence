from distutils.core import setup
import py2exe, os, sys


setup(
    windows = ["main.py"],
    author="Zemus",
    options={
        'py2exe': { 'optimize': 2, 'bundle_files': 1, 'compressed': True,
                    'packages':['pygame'], 
                    'includes':['cursor', 'enemy', 'entities', 'player', 'utils'],
                    'dist_dir': "../build"
        }
        
    },
    zipfile = None
)
