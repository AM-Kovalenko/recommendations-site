from django import template
from reviews.models import *

"""Здесь прописывается логика работы нового тэга
"""

register = template.Library()  # создание экземпляра класса Library, через которого происходит регистрация собственных шаблонных тэгов


# созданный ТЭГ которй возвращает список категорий
@register.simple_tag(name='getcats')
def get_categories():
    return Category.objects.all()


# @register.inclusion_tag('reviews/list_categories.html')
# def show_categories():
#     cats = Category.object.all()
#     return {"cats": cats}

# # созданный ТЭГ которй возвращает список категорий
# @register.simple_tag(name='getcats')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else: return Category.objects.filter(pk=filter)
#
#
# # созданный включающий ТЭГ(формирует фрагмент html-страницы, которую возвращает)
# @register.inclusion_tag('reviews/list_categories.html')
# def show_categories(sort=None, cat_selected=0):
#     if not sort:
#         cats = Category.objects.all()
#     else:
#         cats = Category.objects.order_by(sort)
#     return {"cats": cats, "cat_selected": cat_selected}
