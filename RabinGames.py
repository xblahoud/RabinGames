# -*- coding: utf-8 -*-
"""
Visualisation of Rabin Games.
-----------------------------

Library for RG visualisation and (in the future) solving. The class game
can now compute the green sets.

@author: xblahoud
"""
__all__ = ['Node', 'Game']

import os
import re
#import IPython.display

#TODO Check whether all succ are defined
#TODO Node.copy(), Game.copy()
#TODO Game.invert_players()

from FrozenSetset import FrozenSetset

SYSTEM = 1
ENV = 0
DOT_STRING = '\n--DOT--\n'

class Node(object):
    '''
    The class `Node` represents nodes of the game.
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
        temp = line.split('*')
        self.type, self.id = Node._parse_type_and_id(temp[0].strip())
        self.green = frozenset(temp[1].split())
        self.red = frozenset(temp[2].split())
        self.succ = list(temp[3].split())
        self.S = None

    @staticmethod
    def _parse_type_and_id(id_str):
        '''Gets type and id from a parenthesized id.
        '''
        env = re.compile(r'\[(\d+)\]')
        sys = re.compile(r'\((\d+)\)')
        if env.match(id_str):
            return ENV, env.match(id_str).group(1)
        if sys.match(id_str):
            return SYSTEM, sys.match(id_str).group(1)

    def __repr__(self):
        result = ''
        if self.type == ENV:
            result += "["+self.id+"]:"
        else:
            result += "("+self.id+"):"
        if self.green:
            result += "\n  green sets: " + self.green.__repr__()
        if self.red:
            result += "\n  red sets: " + self.red.__repr__()
        result += "\n  successors: " + self.succ.__repr__()
        if self.S is not None:
            result += "\n  S(" + self.id + ") = " + self.S.__repr__()
        return result

    def get_dot(self):
        '''
        Returns a dot representation of the node and edges to
        the node's successor.
        '''
        result = '  ' + self.id + ' [label=<'
        if self.S is not None:
            result += '<FONT COLOR="green">' +\
                self.S.__repr__() +\
                '</FONT><BR/>'
        result += self.id
        if self.green:
            result += '<BR/><FONT COLOR="green">' +\
                '{' + ','.join(self.green) + '}' + '</FONT>'
        if self.red:
            result += '<BR/><FONT COLOR="red">' +\
                '{' + ','.join(self.red) + '}' + '</FONT>'
        result += '>'
        if self.type == ENV:
            result += ',shape="box"'
        result += ']'
        for destination in self.succ:
            # TODO succ:id -> ref
            result += '\n    ' + self.id + ' -> ' + destination
        return result

    def remove_reds_from_setset(self, setset):
        '''
        Returns a copy of the given setset which does not contain innersets
        that contains some of the node.red sets
        '''
        tmp = setset.copy()
        for red in self.red:
            tmp = tmp.remove_all_with(red)
        return tmp

class Game(object):
    '''
    Objects of class `Game` represent Rabin games. They consist of
    a graph where the nodes aree of two types:

    * SYSTEM 1
    * ENVIRONMENT 0

    `dot_attr` are arguments send to dot. It expects to be a (possibly)
    multiline string.
    '''
    node_class = Node
    setset_class = FrozenSetset
    def __init__(self, game_str=None, filename=None, dot_attr=None,
                 dot_string=DOT_STRING):
        self.preds = {} # stores the predecessor relation
        self.id_to_node = {} # maps ids to node objects
        self.nodes = list() # store all the nodes
        self.dot_attr = dot_attr

        if filename is not None:
            with open(filename, 'r') as file_:
                game_str = file_.read()

        if game_str is not None:
            tmp = game_str.split(dot_string)
            game_str = tmp[0]
            if len(tmp) > 1:
                if self.dot_attr is None:
                    self.dot_attr = tmp[1]
                else:
                    self.dot_attr += '\n' + tmp[1]

            self._read_nodes_from_string(game_str)

        # TODO Redo id's to references in succ?
        ## Make references out of ids in succ relation & fill self.pred
        for node in self.nodes:
            #node.succ = [self.id_to_node[s] for s in node.succ]
            ## Fill the predecessor relation
            for successor in node.succ:
                if successor not in self.preds:
                    self.preds[successor] = list()
                self.preds[successor].append(node)

    def _read_nodes_from_string(self, game_str):
        '''Reads the nodes from the given game_str
        '''
        for node_str in game_str.splitlines():
            if node_str.strip() is '':
                continue
            self._add_node_from_string(node_str)

    def _add_node_from_string(self, node_str):
        '''Creates a new node from the given string and adds it
        into the game graph.
        '''
        node = self.node_class(node_str)
        self.nodes.append(node)
        self.id_to_node[node.id] = node

    def __repr__(self):
        res = ''
        for node in self.nodes:
            res += node.__repr__() + '\n'
        return res

    def to_svg(self):
        '''Returns a string with svg representation of the game.
        It is created by dot.
        '''
        svg_file = '/tmp/game.svg'
        self.svg_to_file(svg_file)
        svg = open(svg_file, 'r').read()
        os.system('rm ' + svg_file)
        return svg

    def svg_to_file(self, filename='game.svg'):
        '''Creates an SVG file with the game.
        '''
        dot_file = '/tmp/game.dot'
        with open(dot_file, 'w') as dot:
            dot.write(self.get_dot())
        os.system('dot -Tsvg ' + dot_file + ' > ' + filename)
        os.system('rm ' + dot_file)

    def _repr_svg_(self):
        '''for Ipython'''
        return self.to_svg()

    def get_dot(self, args=None):
        '''Returns a string with dot representation of the game graph.
        '''
        if args is None:
            args = self.dot_attr
        dot = 'digraph Game {'
        if args is not None and args:
            for line in args.splitlines():
                dot += '\n  ' + line
        for node in self.nodes:
            dot += "\n" + node.get_dot()
        dot += "\n}"
        return dot

    def compute_green_sets(self):
        '''
        Computes the setset of indices, such that the player SYSTEM
        can force to visit some green set for each of the given sets.
        '''
        queue = set() # stores the nodes to process


        ## Fill the queue with predecessors of states that have non-empty S
        for node in self.nodes:
            node.S = self.setset_class(
                    [self.setset_class.innersets_cls([green])
                    for green in node.green]
                    )
            node.S -= self.setset_class(
                    [self.setset_class.innersets_cls([red])
                    for red in node.red]
                    )
            if node.S:
                # Ads predecessors to q
                queue |= set(self.preds[node.id])

        while queue:
            node = queue.pop()
            new = node.S.copy()

            if node.type == SYSTEM:
                for succ_ in node.succ:
                    new |= self.id_to_node[succ_].S
            else:
                new |= (self.setset_class.merge_all([self.id_to_node[succ].S
                        for succ in node.succ]))

            new = new.purify()
            new = node.remove_reds_from_setset(new)

            if new != node.S:
                node.S = new
				# Ads predecessors to q
                queue |= set(self.preds[node.id])

    # TODO def print_to_file(self,filename):

#%%

if __name__ == '__main__':
    TEST_GAME = "[0] * 3 * * 1 2\n" + \
                "(1) * 1 * * 3\n" +\
                "(2) * 2 * * 3\n" +\
                "[3] * * 3 * 4 5\n" +\
                "(4) * * 1 * 0\n" +\
                "(5) * * 2 * 0"

    GAME = Game(TEST_GAME)
    GAME.compute_green_sets()
    #IPython.display.display(GAME)
