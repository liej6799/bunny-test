'''
Copyright (C) 2017-2023 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
cimport cython
from decimal import Decimal

cdef extern from *:
    """
    #ifdef CYTHON_WITHOUT_ASSERTIONS
    #define _COMPILED_WITH_ASSERTIONS 0
    #else
    #define _COMPILED_WITH_ASSERTIONS 1
    #endif
    """
    cdef bint _COMPILED_WITH_ASSERTIONS
COMPILED_WITH_ASSERTIONS = _COMPILED_WITH_ASSERTIONS

cdef dict convert_none_values(d: dict, s: str):
    for key, value in d.items():
        if value is None:
            d[key] = s
    return d
