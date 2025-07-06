import sys
import os

#sys.path.insert(0,  os.path.abspath('../'))

project = 'Immunity docs'
copyright = '2025, light-hat'
author = 'github.com/light-hat'
release = '2.0.0'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinxcontrib.httpdomain",
    "sphinx_rtd_theme",
    'sphinx_copybutton',
    'sphinxcontrib.mermaid',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.imgconverter',
    'autodocsumm', 
    'sphinx.ext.coverage',
]

auto_doc_default_options = {'autosummary': True}

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
