# -*- coding: utf-8 -*-
"""
    getusee
    ~~~~~

    This is a package that simplifies the selenium usage process and can develop software faster.
    However, to improve efficiency, please try to use select method and headless mode.
"""
from .sdriver import smart_driver
from .bdriver import base_checker
from .cupdate import *
from .traversement import *
from .selfcheck import *
from .start import *

__version__ = '1.0.0'
