# -*- coding: utf-8 -*-
"""
Visualisation of Rabin Games.
-----------------------------

Library for RG visualisation and (in the future) solving. The class game
can now compute the green sets.

@author: xblahoud
"""
__all__ = ['NodeColored', 'GameColored']

#import IPython.display
from RabinGames import Node, Game, ENV
from RedGreenSets import RED, GREEN, ColoredFrozenSetset, FrozenRGSet, CInt

class NodeColored(Node):
    '''
    The class `NodeColored` represents nodes of the game. It uses colored
    sets (FrozenRGSet) to represent green and red accepting sets.
    A node of a game is given as a line

    `id * type * g * r * succ`

    * `id` is a name of the node
    * `type` determine the player
        - `0` is the _environment_ `[]`
        - `1` is the _system_ `()`
    * `g` is the list of _green_ sets, use space `' '` as a delimiter
    * `r` is the list of _red_ sets

    The class has also a member `S` for storing the green sets.
    The player `system ()` has a strategy to visit some state from each
    of the green sets in `S`.  The green sets are `not` computed
    at initialization.
    '''
    def __init__(self, line):
        super(NodeColored, self).__init__(line)
        self.green = FrozenRGSet([CInt(i, GREEN) for i in self.green])
        self.red = FrozenRGSet([CInt(i, RED) for i in self.red])

    def get_dot(self):
        '''
        Returns a dot representation of the node and edges to
        the node's successor.
        '''
        result = '  ' + self.id + ' [label=<'
        if self.S is not None:
            result += self.S.to_html() + '<BR/>'
        result += self.id
        if self.green:
            result += '<BR/>' + self.green.to_html()
        if self.red:
            result += '<BR/>' + self.red.to_html()
        result += '>'
        if self.type == ENV:
            result += ',shape="box"'
        result += ']'
        for destination in self.succ:
            result += '\n    ' + self.id + ' -> ' + destination
        return result

    def remove_reds_from_setset(self, setset):
        tmp = setset.copy()
        for red in self.red:
            tmp = tmp.remove_all_with(CInt(red.val, GREEN))
        return tmp

class GameColored(Game):
    '''
    Objects of class `GameColored` represent Rabin games. They consist of
    a graph where the nodes aree of two types:

    * SYSTEM 1
    * ENVIRONMENT 0

    `dot_attr` are arguments send to dot. It expects to be a (possibly)
    multiline string.
    '''
    node_class = NodeColored
    setset_class = ColoredFrozenSetset

#%%
if __name__ == '__main__':
    TEST_GAME = "[0] * 3 * * 1 2\n" + \
                "(1) * 1 * * 3\n" +\
                "(2) * 2 * * 3\n" +\
                "[3] * * 3 * 4 5\n" +\
                "(4) * * 1 * 0\n" +\
                "(5) * * 2 * 0"

    GAME = GameColored(TEST_GAME)
    GAME.compute_green_sets()
    #IPython.display.display(GAME)
