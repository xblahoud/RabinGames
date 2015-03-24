# -*- coding: utf-8 -*-
"""
Implementation of multilevel sets that store only integers that are
either red or green. A colored integer is a named tuple (int, color).

@author: xblahoud
"""

from collections import Iterable, namedtuple
from IPython.display import display

GREEN = 'g'
RED = 'r'
BLUE = 'b'
COLORS = [GREEN, RED, BLUE]
color_to_html = {
    RED: 'red',
    GREEN: 'green',
    BLUE: 'blue',
    }

class CInt(namedtuple('CInt', 'val color')):
    def _repr_html_(self):
        return '<font color=' + color_to_html[self.color] + '>' +\
            str(self.val) + '</font>'

def is_int_of_colors(iterable=None):
    '''Decorator which returns a function that checks that given colored
    integer is of an *allowed* color, i.e. color from the iterable..
    '''
    if not isinstance(iterable, Iterable):
        raise TypeError('The is_int_of_colors function needs an iterable' +\
            'of single-character strings')
    if [x for x in iterable if x not in COLORS]:
        raise ValueError('The colors has to be one of COLORS:' +\
            COLORS.__str__())
    def color_in_iterable(c_int):
        '''Just returns whether the given CInt is in the colors listed
        '''
        return c_int.color in iterable
    return color_in_iterable

is_green = is_int_of_colors([GREEN])
is_red = is_int_of_colors([GREEN])
is_rg = is_int_of_colors([GREEN, RED])

class FrozenRGSet(frozenset):
    def __init__(self, iterable=None):
        if iterable is not None:
            non_rg = [x for x in iterable if not is_rg(x)]
            if non_rg:
                raise ValueError('Accepts only numbers of green ' +\
                    'or red color! Wrong values are: ' + str(non_rg))
        super(FrozenRGSet, self).__init__(iterable)
    
    def _repr_html_(self):
        return '{' + ','.join([elem._repr_html_() for elem in self]) + '}'

if __name__ == '__main__':
    g3 = CInt(3,GREEN)
    b2 = CInt(2,BLUE)
    r1 = CInt(1,RED)
    #a = FrozenRGSet([g3,b2])
    b = FrozenRGSet([g3,r1])