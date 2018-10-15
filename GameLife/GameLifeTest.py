import unittest
import GameLifeLibrary as Lib
import random


class GameLifeTest(unittest.TestCase):
    def testStr(self):
        fish = Lib.GameLife.FishUnit()
        self.assertEqual(fish.str(), 'f')

    def testStrToUnit(self):
        n, m, k = 15, 20, 10
        a = self.GenerateTable(n, m)
        game = Lib.GameLife(n, m, k, a)
        self.assertTrue(isinstance(game.StrToUnit('r'), Lib.GameLife.RockUnit))

    def testInit(self):
        n, m, k = 4, 4, 10
        a = [['f', 's', 'n', 'r'],
             ['r', 'n', 's', 'f'],
             ['n', 'r', 'f', 's'],
             ['s', 'n', 'r', 'f']]
        game = Lib.GameLife(n, m, k, a)
        for i in range(n):
            for j in range(m):
                self.assertEqual(a[i][j], game.field_[i][j].str())
        self.assertEqual(k, game.k_)

    def GenerateTable(self, n, m):
        a = [[0] * m for i in range(n)]
        c = ['f', 's', 'n', 'r']
        for i in range(n):
            for j in range(m):
                random.shuffle(c)
                a[i][j] = c[0]
        return a

    def testNeighborsCnt(self):
        n, m, k = 4, 4, 10
        a = [['f', 's', 'n', 'r'],
             ['r', 'n', 's', 'f'],
             ['n', 'f', 'f', 's'],
             ['s', 'n', 'r', 'f']]
        game = Lib.GameLife(n, m, k, a)
        self.assertEqual(game.GetNeighborsCnt(1, 1, 'f'), 3)
        self.assertEqual(game.GetNeighborsCnt(2, 3, 'n'), 0)
        self.assertEqual(game.GetNeighborsCnt(3, 2, 's'), 1)

    def checkOneStep(self, n, m, k, a, ans):
        game = Lib.GameLife(n, m, k, a)
        game.OneStep()
        for i in range(n):
            for j in range(m):
                self.assertEqual(ans[i][j], game.field_[i][j].str())

    def testOneStep(self):
        n, m, k = 4, 4, 10
        a = [['f', 's', 'n', 'r'],
             ['r', 'n', 's', 'f'],
             ['n', 'f', 'f', 's'],
             ['s', 'n', 'r', 'f']]
        ans = [['n', 'n', 'n', 'r'],
               ['r', 'f', 's', 'n'],
               ['n', 'n', 'f', 'n'],
               ['n', 'n', 'r', 'n']]
        self.checkOneStep(n, m, k, a, ans)
        n, m, k = 3, 3, 7
        a = [['f', 's', 'n'],
             ['r', 'n', 'f'],
             ['s', 'r', 'f']]
        ans = [['n', 'n', 'n'],
               ['r', 'f', 'n'],
               ['n', 'r', 'n']]
        self.checkOneStep(n, m, k, a, ans)


if (__name__ == '__main__'):
    unittest.main()
