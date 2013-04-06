from StringIO import StringIO
import parse_blast

class testParseBlastn():
    def setUp(self):
        self.blast_output = "small_blastn_search.txt"
        self.HSP_output = open("small_blastn_HSP.txt", "r").readlines()
        self.parsed_output = "small_blastn_output.txt"
        self.blast_expected = open(self.parsed_output, "r").readlines()

    def test_blast_table_consumer(self):
        line = 0
        for i in parse_blast.blast_table_consumer(self.blast_output):
            assert i == eval(self.HSP_output[line])
            line += 1

    def test_blast_output(self):
        line = 0
        for i in parse_blast.blast_table_consumer(self.blast_output):
            assert parse_blast.write_parsed(i) ==\
                self.blast_expected[line].strip()
            line += 1
