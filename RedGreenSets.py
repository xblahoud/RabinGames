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
    '''A simple function that sorts the given list and returns its set-like
    string representation, i.e. elements separated by ``,`` in curly
    braces ``{,}``.
    '''
    list_.sort()
    return '{' + ','.join(list_) + '}'

class CInt(namedtuple('CInt', 'val color')):
    '''
    Class that stores colored integers (in fact, no restriction that
    it has to be integer is implemented). A CInt instance has its value
    and color. The possible colors are defined in the COLORS constant.
    '''
    def prefix_repr(self):
        '''Returns a string where the color is prefixed to value.
        '''
        return self.color + str(self.val)

    def _repr_html_(self):
        '''For IPython.display
        '''
        return self.to_html()

    def to_html(self):
        '''Returns a colored representation of the CInt in html
        '''
        return '<FONT color="' + color_to_html[self.color] + '">' +\
            str(self.val) + '</FONT>'

class FrozenRGSet(frozenset):
    '''
    A frozenset which stores CInt objects of only red and green color.
    It can print them in html in colors
    '''
    def __init__(self, iterable=[]):
        '''Expects only ``CInt``s of appropriete colors
        '''
        if not isinstance(iterable, Iterable):
            raise TypeError(type(iterable).__name__ +\
                    " object is not iterable")
        non_rg = [x for x in iterable if not is_rg(x)]
        if non_rg:
            raise ValueError('Accepts only numbers of green ' +\
                'or red color! Wrong values are: ' + str(non_rg))
        super(FrozenRGSet, self).__init__(iterable)

    def __repr__(self):
        '''Returns sorted set-like string with prefixed colors to values
        '''
        return str_sorted_set([elem.prefix_repr() for elem in self])

    def _repr_html_(self):
        '''For IPython.display
        '''
        return self.to_html()

    def to_html(self):
        '''Returns a set-like string with html representation of the elements.
        '''
        return str_sorted_set([elem.to_html() for elem in self])


class ColoredFrozenSetset(FrozenSetset):
    '''A frozen setset class with ``FrozenColoredSet`` (resp. ``FrozenRGSet``)
    objects as innersets. It has a colored representation in html possible
    in addition to ``FrozenSetset``.
    '''
    innersets_cls = FrozenRGSet
    def __repr__(self):
        '''Returns a sorted representation of itself with using the str()
        representation of the innersets.
        '''
        return str_sorted_set([str(oneset) for oneset in self])

    def to_html(self):
        '''Returns a colored and sorted representation of itself in html
        '''
        return str_sorted_set([oneset.to_html() for oneset in self])

    def _repr_html_(self):
        '''For IPython.display. Calls self.to_html()
        '''
        return self.to_html()

if __name__ == '__main__':
    pass
#    g3 = CInt(3, GREEN)
#    g2 = CInt(2, GREEN)
#    g1 = CInt(1, GREEN)
#    #b2 = CInt(2, BLUE)
#    r1 = CInt(1, RED)
#    r2 = CInt(2, RED)
#    a = FrozenRGSet([g1, g2])
#    b = FrozenRGSet([r1, r2])
#    ss = ColoredFrozenSetset([a, b])


