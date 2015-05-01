from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils.datastructures import MultiValueDictKeyError
from survey.models import *


# index view will allow to create a new question
@login_required(login_url="/login/")
def index(request):
    return render(request, 'main.html', {})


# reset password of current user ( ! no old password check)
@login_required(login_url="/login/")
def reset(request):
    if request.method == 'GET':
        return render(request, 'reset.html', {})
    if request.method == 'POST':
        try:
            new = request.POST['new']
            confirm = request.POST['confirm']
            if new != confirm:
                return render(request, 'reset.html',
                                {'error': "Error (invalid confirmation) : new password and confirmation are not similar."})
            if len(new) < 8:
                return render(request, 'reset.html',
                                {'error': "Error (invalid password) : new password must be at least 8 characters long."})
        except MultiValueDictKeyError:
            return render(request, 'reset.html', 
                            {'error': "Error (invalid form) : Please fill the 'new' and 'confirm' parameters before to submit !"})
        request.user.set_password(new)
        request.user.save()
        return redirect('/')


# form to create a new question
@login_required(login_url="/login/")
def question_creation(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        try:
            question_text = request.POST['question']
            delta = int(request.POST['delta'])
        except MultiValueDictKeyError:
            return render(request, 'main.html',
                            {'error': "Error (invalid form) : Please fill the text and delta parameters !"})
        if len(question_text) < 1:
            return render(request, 'main.html',
                            {'error': "Error (invalid value) : Please fill the text parameters !"})
        if delta > 30 or delta < 0:
            return render(request, 'main.html', 
                            {'text': question_text,
                             'error': "Error (invalid value) : Please select a answer delta between 0 and 30 !"})
        answer_date = datetime.now()+timedelta(days=delta)+timedelta(seconds=2)
        question = Question(text=question_text,
                            author=request.user, 
                            answer_date=answer_date)
        question.save()
        return redirect(question.get_absolute_url())


# main question view
@login_required(login_url="/login/")
def question_view(request, token, error=""):
    question = get_object_or_404(Question, token=token)
    try:
        current_user_answer = Answer.objects.get(question=question, author=request.user)
    except ObjectDoesNotExist:
        current_user_answer = None
    delta = (question.answer_date-question.pub_date).days
    return render(request, 'question_view.html', 
                    {'question': question,
                     'delta': delta,
                     'error': error,
                     'current_user_answer': current_user_answer})


# main question view
@login_required(login_url="/login/")
@require_http_methods(["POST"])
def question_answer(request, token):
    question = get_object_or_404(Question, token=token)
    try:
        text = request.POST['text']
    except MultiValueDictKeyError:
        return question_view(request, token, "Error (invalid form) : Please fill the text parameters !")
    if len(text) < 1:
        return question_view(request, token, "Error (invalid value) : Please fill the text parameters !")
    # only update fields text and pub_date if answer already exists
    Answer.objects.update_or_create(question=question,
                                    author=request.user, 
                                    defaults=dict(text=text, pub_date=datetime.now()))
    return redirect(question.get_absolute_url())


# main question view
@login_required(login_url="/login/")
@require_http_methods(["POST"])
def question_edit(request, token):
    question = get_object_or_404(Question, token=token)
    if not question.author == request.user:
        return HttpResponseForbidden
    try:
        text = request.POST['text']
        delta = int(request.POST['delta'])
    except MultiValueDictKeyError:
        return render(request, 'main.html',
                        {'error': "Error (invalid form) : Please fill the text and delta parameters !"})
    if delta > 30 or delta < 0:
        return render(request, 'main.html', 
                        {'text': question_text,
                         'error': "Error (invalid value) : Please select a answer delta between 0 and 30 !"})
    # update fields text and answer_date if question already exists
    question.answer_date = question.pub_date+timedelta(days=delta)
    question.text = text
    question.save()
    return redirect(question.get_absolute_url())
