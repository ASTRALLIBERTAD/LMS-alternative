# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
# ADD THESE LINES AT THE TOP (This is what's missing!)

import os
import sys

# Add your source code directory to Python path
sys.path.insert(0, os.path.abspath('../../src'))

# Print to verify path (you can remove this later)
print("=" * 70)
print("Python path configured for Sphinx:")
print(f"  {sys.path[0]}")
print("=" * 70)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'LMS Alternative'
copyright = '2025, ASTRALLIBERTAD, TagaWasakNgPunoNgSaging'
author = 'ASTRALLIBERTAD, TagaWasakNgPunoNgSaging'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # 'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    # 'sphinx.ext.viewcode',
    # 'sphinx.ext.intersphinx',
    # 'sphinx.ext.autosummary',
    # 'sphinx_autodoc_typehints',
    'myst_parser',
    # 'sphinx_markdown_builder',
]

# Mock imports
autodoc_mock_imports = [
    'flet',
    'google',
    'google.oauth2',
    'google.auth',
    'google_auth_oauthlib',
    'googleapiclient',
    'googleapiclient.discovery',
    'googleapiclient.errors',
    'googleapiclient.http',
]

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'

# Autosummary settings
autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}