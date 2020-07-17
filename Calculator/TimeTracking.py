import timeit


def stop_timer(start, function_name):
    stop = timeit.default_timer()
    print('Time Elapsed on {0} : {1}'.format(function_name, stop - start))
    return


def get_cur_timer():
    return timeit.default_timer()
