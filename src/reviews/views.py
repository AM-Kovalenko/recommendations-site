from django.shortcuts import render


# функция представления главной страницы -> переделываю в класс представления (основанном на базовом классе ListView)
def index(request):
    return render(request, 'reviews/index.html')
