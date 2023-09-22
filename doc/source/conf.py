# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import sys
from pathlib import Path

src_path = Path("../..").resolve()  # absolute path to root source code folder
sys.path.insert(0, str(src_path))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "HeatPumpSimulation"
copyright = "2023, Frederic Bless & Cecilia Dean"
author = "Frederic Bless & Cecilia Dean"
release = "0.0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# -- Extension configuration -------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx_autodoc_typehints",
    "sphinx_autodoc_defaultargs",
    "sphinx_gallery.gen_gallery",
]

# -- Options for Autodoc extension ----------------------------------------------
# This value selects if automatically documented members are sorted alphabetical
# (value 'alphabetical'), by member type (value 'groupwise') or by source order
# (value 'bysource'). The default is alphabetical.
autodoc_member_order = "bysource"
# -- Options for Napoleon extension ----------------------------------------------
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = False
# -- Options for autosectionlabel extension --------------------------------------
# Make sure the target is unique
autosectionlabel_prefix_document = True
# -- Options for typehints extension ---------------------------------------------
typehints_document_rtype = True
typehints_use_rtype = True
# -- Options for Intersphinx extension ----------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
#    "numpy": ("https://numpy.org/doc/stable/", None),
#    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "sklearn": ("https://scikit-learn.org/stable", None),
}
# -- Options for Default arguments extension ----------------------------------
rst_prolog = """
.. |default| raw:: html

    <div class="default-value-section"><span class="default-value-label">Default:</span>
    """
# -- Options for Gallery extension ----------------------------------------------
# https://sphinx-gallery.github.io/stable/configuration.html
sphinx_gallery_conf = {
    # path to your example scripts
    "examples_dirs": [
        "../../examples",
    ],
    # path to where to save gallery generated output
    "gallery_dirs": ["auto_examples"],
    # directory where function granular galleries are stored
    "backreferences_dir": "auto_modules/backreferences",
    # do not reset on each example
    #'reset_modules': (),
    # do not capture matplotlib output
    # https://sphinx-gallery.github.io/stable/configuration.html#prevent-capture-of-certain-classes
    'ignore_repr_types': r'matplotlib[.](text|axes|legend|lines)',
    # Show memeory usage
    'show_memory': False,
}
