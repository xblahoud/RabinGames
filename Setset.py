""" Implementation of a set of sets """

class Setset(set):
    """
    A setset object represents a set of sets. The inner sets are
    frozensets.
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
        Returns a merge ($otimes$) of itself and the other Setset.
        S_1 otimes S_2 = {a cup b | a in S_1, b in S_2}
        '''
        if other is None:
            return self
        return Setset([s1 | s2 for s1 in self for s2 in other])

    def merge_update(self, other):
        '''
        Merges ($otimes$) itself with the other Setset.
        S_1 otimes S_2 = {a cup b | a in S_1, b in S_2}
        '''
        result = self.merge(other)
        self.clear()
        self.update(result)

    @classmethod
    def merge_all(cls, iterable=None):
        '''
        Merges all setsets given in iterable.
        If only one setset in the iterable given, it retruns it unmodified.
        If the iterable is empty, returns an empty set.
        '''
        if iterable is None or len(iterable) == 0:
            return cls()
        result = cls([frozenset()])
        for setset in iterable:
            result.merge_update(setset)
        return result

    def purify(self):
        '''
        Removes supersets from the setset, i.e. makes the setset an antichain.
        '''
        tmp = self.copy()
        for subset in tmp:
            self -= self.__get_supersets__(subset)

    def remove_all_with(self, element):
        '''
        Removes all (inner)sets that contain the element given from the setset.
        '''
        tmp = self.copy()
        for innerset in tmp:
            if element in innerset:
                self.remove(innerset)
