"""
Provides a Python package based on the Model-View-ViewModel architectural pattern.
"""

from .model import Model
from .view import View, LoginView
from .viewmodel import ViewModel

__all__ = ["Model", "View", "ViewModel", "Login"]