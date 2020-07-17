from django.shortcuts import render
from Calculator import user_interface

# Create your views here.
def landing(request):
    if request.POST and request.FILES:
        print(request.FILES)
        user_interface.handle_uploaded_file(request.FILES['csvfile'])
        user_interface.initialize_words()
    elif request.POST:
        print("post method")
        user_interface.set_params(request.POST['time_for_solution_search'],
                                  request.POST['words_number'],
                                  request.POST['attempts_num'],
                                  request.POST['template_first_id'],
                                  request.POST['template_last_id'],
                                  request.POST['json_base_name'])
        user_interface.generate_num_crosswords(request.POST['attempts_num'])
    return render(request, "CrossGen.html", {"current_level": user_interface.json_base_name})

def view_jsons(request):
    cur_level = request.GET['lev']
    json_files = user_interface.get_all_jsons(cur_level)
    return render(request, "OutputViewer.html", {"json_files": json_files})
