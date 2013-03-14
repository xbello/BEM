from StringIO import StringIO
import parse_blast

class testParseBlast():
    def setUp(self):
        self.blast_output = "tests/output.blast"
        self.parsed_output = "tests/test_parse_blast.txt"
        from tests.output_blast import HSP
        self.blast_expected = HSP

    def test_blast_table_consumer(self):
        for i in parse_blast.blast_table_consumer(self.blast_output):
            assert i == self.blast_expected
            break

    def test_write_parsed(self):
        output = StringIO()
        for HSP in parse_blast.blast_table_consumer(self.blast_output):
            parse_blast.write_parsed(output, HSP)

        output.seek(0)
        assert output.readlines() == open(self.parsed_output, "r").readlines()

