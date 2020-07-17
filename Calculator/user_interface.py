import random
import json
import os
from os import listdir
from Calculator import FillCrossword
from Calculator import FileManagement
from Calculator import TimeTracking
from Calculator.crossword import *

len_distribution_list = [0] * 16
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input/example.txt')
Data = FileManagement.read_from_file(path)
words_list = Data[1]
words_dict = Data[0]
sorted_words_list = FileManagement.sort_list_by_len(words_list)


def get_random_template(first_index, last_index):
    template_index = random.randint(first_index, last_index)
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)),f'{template_folder}/template{template_index}.txt')
    template = path
    return template


def get_random_words_by_len():
    ret_list = []
    count_nonzeros = sum(len_distribution_list)
    print(f'crossword contains {count_nonzeros} words')
    for i in range(len(len_distribution_list)):
        if len_distribution_list[i] > 0:
            multiplayer = len_distribution_list[i] * words_number/count_nonzeros
            random_words_with_len = random.sample(sorted_words_list[i], int(multiplayer))
            ret_list.extend(random_words_with_len)
    return ret_list


def get_all_words_by_len(crossword):
    global len_distribution_list
    len_distribution_list = [0] * 16
    for var in crossword.variables:
        len_distribution_list[var.length-1] += 1


def assignment_to_json(assignment, crossword, id):
    json_words = []
    for var, word in assignment.items():
        json_words.append({"answer": word, "isHorizontal": var.isHorizontal, "pos": {"x": var.i, "y": var.j}, "question": words_dict[word][0].rstrip()})
    sort_by_pos = sorted(json_words, key=lambda k: (k['pos']['x'], k['pos']['y']))
    json_string = {"level":
                        {"id": id,
                         "size": {"width": crossword.width, "height": crossword.height},
                         "words" : sort_by_pos
                         }
                   }
    print(json_string)
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'json/{json_base_name}')
    filename = f'{json_base_name}_{id}.json'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + '/' + filename, 'w', encoding="utf8", errors='ignore') as outfile:
        json.dump(json_string, outfile)


def generate_crossword(template, id):
    start = TimeTracking.get_cur_timer()
    # Generate crossword
    crossword = Crossword(template, '_')
    get_all_words_by_len(crossword)
    random_word_list = get_random_words_by_len()
    crossword.set_words(random_word_list)
    creator = FillCrossword.CrosswordCreator(crossword, time_for_solution_search)  # input : crossword, maximum time for one generation
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
        return False
    else:
        creator.print(assignment)
        assignment_to_json(assignment, crossword, id)
        TimeTracking.stop_timer(start, 'crossword generation')
        return True


def generate_num_crosswords(num):
    start = TimeTracking.get_cur_timer()
    successful = 0
    for i in range(0, int(num)):
        template = get_random_template(template_first_id, template_last_id)
        print(f'starting try to solve crossword # {i} out of {num}. Randomly chosen template is {template}. Successful count is {successful} ')
        if generate_crossword(template, successful):
            successful += 1
        print()
    TimeTracking.stop_timer(start, f" {num} crosswords creation. Successfully created = {successful} out of {num}")


template_folder = 'templates'   #name of folder for templates


json_base_name = 'level_3'  # name of folder created in "json" and also start name of json files created


time_for_solution_search = 3  #in seconds. The bigger time - the bigger solution find percentage
words_number = 100      # Number of words in pool for filling the crossword. Optimal 100-300.
attempts_num = 100      # Number of attempts to create crossword.
template_first_id = 1   #id of first template file in folder "templates"
template_last_id = 1   #id of last template file in folder "templates"


def set_params(time, word_num, attempts, first_templ, last_templ, json_base):
    global time_for_solution_search, words_number, attempts_num, template_first_id, template_last_id, json_base_name
    time_for_solution_search = int(time)
    words_number = int(word_num)
    attempts_num = int(attempts)
    template_first_id = int(first_templ)
    template_last_id = int(last_templ)
    json_base_name = json_base

def handle_uploaded_file(f):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'input\example.txt')
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def initialize_words():
    global Data, words_list, words_dict, sorted_words_list
    Data = FileManagement.read_from_file(path)
    words_list = Data[1]
    words_dict = Data[0]
    sorted_words_list = FileManagement.sort_list_by_len(words_list)


def get_all_jsons(lev):
    ret_arr = []
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'json/{lev}')
    for f in listdir(path):
        with open(path + "/"+f, 'r', encoding="utf8", errors='ignore') as json_obj:
            ret_arr.append(json.loads(json_obj.read()))
    return ret_arr

# generate_num_crosswords(attempts_num)
