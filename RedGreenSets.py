# -*- coding: utf-8 -*-
"""
Implementation of multilevel sets that store only integers that are
either red or green. A colored integer is a named tuple (int, color).

@author: xblahoud
"""

__all__ = ['GREEN', 'RED', 'BLUE', 'CInt', 'FrozenRGSet', 'ColoredFrozenSetset']

from collections import Iterable, namedtuple
from FrozenSetset import FrozenSetset
#from IPython.display import display

GREEN = 'g'
RED = 'r'
BLUE = 'b'
COLORS = [GREEN, RED, BLUE]
color_to_html = {
    RED: 'red',
    GREEN: 'green',
    BLUE: 'blue',
    }

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
        if not isinstance(c_int, CInt):
            raise TypeError('CInt expected, ' +\
                type(c_int).__name__ + ' given.')
        return c_int.color in iterable
    return color_in_iterable

is_green = is_int_of_colors([GREEN])
is_red = is_int_of_colors([GREEN])
is_rg = is_int_of_colors([GREEN, RED])

def str_sorted_set(list_):
    list_.sort()
    return '{' + ','.join(list_) + '}'

class CInt(namedtuple('CInt', 'val color')):
    def prefix_repr(self):
        return self.color + str(self.val)

    def _repr_html_(self):
        return self.to_html()

    def to_html(self):
        return '<FONT color="' + color_to_html[self.color] + '">' +\
            str(self.val) + '</FONT>'

class FrozenRGSet(frozenset):
    def __init__(self, iterable=None):
        if iterable is not None:
            non_rg = [x for x in iterable if not is_rg(x)]
            if non_rg:
                raise ValueError('Accepts only numbers of green ' +\
                    'or red color! Wrong values are: ' + str(non_rg))
        super(FrozenRGSet, self).__init__(iterable)

    def __repr__(self):
        return str_sorted_set([elem.prefix_repr() for elem in self])

    def _repr_html_(self):
        return self.to_html()

    def to_html(self):
        return str_sorted_set([elem.to_html() for elem in self])


class ColoredFrozenSetset(FrozenSetset):
    innersets_cls = FrozenRGSet
    def __repr__(self):
        return str_sorted_set([str(oneset) for oneset in self])

    def to_html(self):
        return str_sorted_set([oneset.to_html() for oneset in self])

    def _repr_html_(self):
        return self.to_html()

if __name__ == '__main__':
    g3 = CInt(3, GREEN)
    g2 = CInt(2, GREEN)
    g1 = CInt(1, GREEN)
    #b2 = CInt(2, BLUE)
    r1 = CInt(1, RED)
    r2 = CInt(2, RED)
    a = FrozenRGSet([g1, g2])
    b = FrozenRGSet([r1, r2])
    ss = ColoredFrozenSetset([a, b])


