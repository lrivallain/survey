from django.contrib import admin
from survey.models import *


# customize the question admin forms and display
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('token', 'pub_date', 'author')
    list_filter = ['pub_date', 'author']

    # auto save the current user as author
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


# customize the answer admin forms and display
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('author', 'question', 'pub_date')
    list_filter = ['question', 'pub_date', 'author']

    # auto save the current user as author
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


# register models to admin interface
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)