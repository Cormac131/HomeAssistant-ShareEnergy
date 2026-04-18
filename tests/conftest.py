"""Add the component directory to sys.path so parser.py and const.py can be
imported as standalone modules without triggering __init__.py (which needs homeassistant)."""
import sys
import os

COMPONENT_DIR = os.path.join(os.path.dirname(__file__), "..", "custom_components", "share_energy")
sys.path.insert(0, os.path.abspath(COMPONENT_DIR))
