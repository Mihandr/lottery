import requests
from bs4 import BeautifulSoup

from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from json import loads
from .models import Person, Winners


def index(request):
    return redirect('/lottery')


def start(request):
    people = Person.objects.all()
    count = people.count()
    if count < 2:
        return HttpResponse("Слишком мало участников!")

    page = requests.get("https://www.random.org/integers/?num=1&min=1&max=1000&col=5&base=10&format=html&rnd=new")
    soup = BeautifulSoup(page.text, 'html.parser')
    random_prize = soup.find_all('pre')[0].get_text()

    page = requests.get("https://www.random.org/integers/?num=1&min=1&max=" + repr(count)
                        + "&col=5&base=10&format=html&rnd=new")
    soup = BeautifulSoup(page.text, 'html.parser')
    random_participant = soup.find_all('pre')[0].get_text()
    winner = people[int(random_participant)]
    Winners.objects.create(first_name=winner.first_name, last_name=winner.last_name, age=winner.age,
                           city=winner.city, win_summ=int(random_prize))
    result_json = {"first_name": winner.first_name, "last_name": winner.last_name, "age": winner.age,
                   "city": winner.city, "win_summ": int(random_prize)}
    people.delete()
    return JsonResponse(result_json, safe=False)


@csrf_exempt
def participant(request):
    people = Person.objects.all()
    if request.method == 'POST':
        list_data = []
        json_data = loads(request.body)
        if isinstance(json_data, dict):
            list_data = list(json_data.values())
        else:
            for json_value in json_data:
                list_data.append(list(json_value.values())[0])
        if len(list_data) != 4:
            return HttpResponse("Должно быть 4 параметра. first_name, last_name, age, city")
        else:
            first_name_in = Person.objects.filter(first_name=list_data[0]).exists()
            last_name_in = Person.objects.filter(last_name=list_data[1]).exists()
            if first_name_in and last_name_in:
                return HttpResponse("В наборе есть объекты с такими именем и фамилией")
            else:
                try:
                    Person.objects.create(first_name=list_data[0], last_name=list_data[1],
                                          age=list_data[2], city=list_data[3])
                except:
                    return HttpResponse("Ошибка. Проверьте формат")
    result_json = []
    for person in people:
        result_json.append({"first_name": person.first_name, "last_name": person.last_name,
                            "age": person.age, "city": person.city})
    return JsonResponse(result_json, safe=False)


def lottery_index(request):
    return redirect('/lottery/participant')


def winners(request):
    win_people = Winners.objects.all()
    result_json = []
    for win_person in win_people:
        result_json.append({"first_name": win_person.first_name, "last_name": win_person.last_name,
                            "age": win_person.age, "city": win_person.city, "win_summ": win_person.win_summ})
    return JsonResponse(result_json, safe=False)
