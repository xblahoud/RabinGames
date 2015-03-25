""" Implementation of a set of sets """

class FrozenSetset(frozenset):
    """
    A FrozenSetset object represents a set of sets. The inner sets
    are also frozen.  In addition to a normal set of sets it also
    implements method merge (x).

    $S_1 (x) S_2 = \{a \cup b\ | a\in S_1, b \in S_2}$.
    """
    #def __init__(self):
    #    self.sets = set()

    def __repr__(self):
        # tmp_list = ['{' + s + '}' for s in self.sets]
        if not self:
            return '{}'
        tmp = ['{' + ','.join(oneset) + '}' for oneset in self]
        return '{' + ','.join(tmp) + '}'

    def __get_supersets__(self, subset):
        '''
        Returns a list of frozensets, that are strict supersets of 'subset'.
        '''
        supersets = set()
        for set_to_check in self:
            if subset < set_to_check:
                supersets.add(set_to_check)
        return supersets

    def merge(self, other=None):
        '''
        Returns a merge ($otimes$) of itself and the other FrozenSetset.
        S_1 otimes S_2 = {a cup b | a in S_1, b in S_2}
        '''
        if other is None:
            return self
        return FrozenSetset([s1 | s2 for s1 in self for s2 in other])

    @classmethod
    def merge_all(cls, iterable=None):
        '''
        Merges all FrozenSetsets given in iterable.
        If only one FrozenSetset in the iterable given, retruns its copy.
        If the iterable is empty, returns an empty FrozenSetset.
        '''
        if iterable is None or len(iterable) == 0:
            return cls()
        result = cls([frozenset()])
        for fsetset in iterable:
            result = result.merge(fsetset)
        return result

    def purify(self):
        '''
        Removes supersets from the FrozenSetset, i.e.returns an antichain.
        '''
        tmp = self.copy()
        for subset in self:
            tmp = tmp.difference(tmp.__get_supersets__(subset))
        return tmp

    def remove_all_with(self, element):
        '''
        Removes from the FrozenSetset all (inner)sets that contain
        the `element` given.
        '''
        tmp = self.copy()
        for innerset in self:
            if element in innerset:
                tmp = tmp.difference([innerset])
        return tmp


if __name__ == '__main__':
    a = FrozenSetset.from_string_list(['a,b', 'c,d'])
    b = FrozenSetset.from_string_list(['1,2', '3,4'])
    c = a.merge(b)
    d = a.union(c)
    