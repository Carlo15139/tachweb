# -*- coding: utf-8 -*-
import os
import sys
import tachyonic_sphinx

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinxcontrib.napoleon',
]

source_suffix = '.rst'

master_doc = 'index'

project = "$description"
copyright = "$copyright"
author = "$authors_string"

version = "$version"
release = version
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'tachyonic'

htmlhelp_basename = '$package' + 'FrameworkDoc'
