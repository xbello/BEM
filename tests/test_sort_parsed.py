import sort_parsed

def check_sorting(input_filename, output_filename):
    input_sorted = sort_parsed.sort_file(input_filename)

    output_lines = open(output_filename, "r").readlines()
    output_values = [x.split() for x in output_lines]

    print input_sorted
    print output_values

    assert input_sorted == output_values

def test_sort():
    '''Check the read, sort and correctness of sorting'''
    check_sorting("tests/test_sort_unsorted.txt",
                  "tests/test_sort_sorted.txt")
    
