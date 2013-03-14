import chao_join

class testChaoJoin():
    def setUp(self):
        self.file_h = open("tests/test_chao_join_unjoin.txt", "r").readlines()

    def test_gap(self):
        assert (chao_join.gap(100, 5, 5) == 505)
        assert (chao_join.gap(100, 5, 5) != 500)

    def test_calc_diagonals(self):
        '''Test that penalty is being well calculated'''
        assert chao_join.calc_diagonals(self.file_h[0], self.file_h[1]) ==\
            (-690, -62)
