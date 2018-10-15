from abc import ABCMeta, abstractmethod


class GameLife:
    class Unit:
        def str(self):
            raise NotImplementedError(
                'Определите str в %s.' % (self.__class__.__name__))

        def NextCondition(self, underself, i, j):
            raise NotImplementedError(
                'Определите NextCondition в %s.' % (self.__class__.__name__))

    class FishUnit(Unit):
        def str(self):
            return 'f'

        def NextCondition(self, underSelf, i, j):
            fishCnt = underSelf.GetNeighborsCnt(i, j, 'f')
            if fishCnt > 3 or fishCnt < 2:
                return GameLife.NonUnit()
            else:
                return GameLife.FishUnit()

    class ShrimpUnit(Unit):
        def str(self):
            return 's'

        def NextCondition(self, underSelf, i, j):
            shrimpCnt = underSelf.GetNeighborsCnt(i, j, 's')
            if shrimpCnt > 3 or shrimpCnt < 2:
                return GameLife.NonUnit()
            else:
                return GameLife.ShrimpUnit()

    class RockUnit(Unit):
        def str(self):
            return 'r'

        def NextCondition(self, underSelf, i, j):
            return GameLife.RockUnit()

    class NonUnit(Unit):
        def str(self):
            return 'n'

        def NextCondition(self, underSelf, i, j):
            fishCnt = underSelf.GetNeighborsCnt(i, j, 'f')
            shrimpCnt = underSelf.GetNeighborsCnt(i, j, 's')
            if fishCnt == 3:
                return GameLife.FishUnit()
            elif shrimpCnt == 3:
                return GameLife.ShrimpUnit()
            else:
                return GameLife.NonUnit()

    def IsCorrect(self, i, j):
        return i >= 0 and j >= 0 and i < self.n_ and j < self.m_

    def GetNeighborsCnt(self, i, j, c):
        cnt = 0
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if ((x != i or y != j) and self.IsCorrect(x, y) and
                   self.field_[x][y].str() == c):
                    cnt += 1
        return cnt

    def Print(self, outstream):
        for i in range(self.n_):
            for j in range(self.m_):
                print(self.field_[i][j].str(), end='', file=outstream)
            print()

    def StrToUnit(self, c):
        units = {
            'f': GameLife.FishUnit(),
            's': GameLife.ShrimpUnit(),
            'n': GameLife.NonUnit(),
            'r': GameLife.RockUnit()
            }
        ans = units.get(c)
        if ans is None:
            raise TypeError
        return ans

    def OneStep(self):
        cur = [[0] * self.m_ for i in range(self.n_)]
        for i in range(self.n_):
            for j in range(self.m_):
                cur[i][j] = self.field_[i][j].NextCondition(self, i, j)
        self.field_ = cur

    def __init__(self, n, m, k, field):
        self.n_, self.m_, self.k_ = n, m, k
        self.field_ = [[0] * m for i in range(n)]
        for i in range(self.n_):
            for j in range(self.m_):
                self.field_[i][j] = self.StrToUnit(field[i][j])

    def Run(self, outstream):
        for i in range(self.k_):
            self.OneStep()
        self.Print(outstream)
