from collections import defaultdict


def read_from_file(filename):
    with open(filename) as f:
        input_lines = [line.split("\t") for line in f]
    output_dict = {}
    output_array = []
    for line in input_lines:
        output_dict[line[0]] = line[1:]
        output_array.append(line[0])
    return [output_dict, output_array]


def write_to_file(filename, list_to_save):
    f = open(filename, 'w')
    f.write(str(list_to_save))


def sort_list_by_len(lst):
    group_by_len = defaultdict(list)
    for ele in lst:
        group_by_len[len(ele)].append(ele)
    res = []
    for key in sorted(group_by_len):
        res.append(group_by_len[key])
    return res
