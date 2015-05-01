from django.db import models
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone
from datetime import datetime, timedelta

# Tocken settings
TOKEN_LENGTH=20
TOKEN_REF_SETS=string.ascii_letters + string.digits
# Generate a random token with TOKEN_LENGTH characters from TOKEN_REF_SETS
def _createToken():
    while True:
        # build a random hash
        token = ''.join([random.choice(TOKEN_REF_SETS) for n in range(TOKEN_LENGTH)])
        # test if token is already in Pool table
        if not Question.objects.filter(token=token):
            return token # if not, return


class Question(models.Model):
    """
        Define a question and its author
    """
    token = models.CharField(max_length=TOKEN_LENGTH, default=_createToken, primary_key=True, editable=False)
    text = models.TextField()
    author = models.ForeignKey(User, editable=False, null=True, blank=True)
    pub_date = models.DateTimeField('date published', editable=False, auto_now_add=True)
    answer_date = models.DateTimeField('answer publication date', default=datetime.now()+timedelta(days=2))

    def __str__(self):
        return self.token

    # get all answers related to the current question
    #  excluding the author one
    def get_all_answers(self):
        return Answer.objects.filter(question=self).exclude(author=self.author)

    # get only author answer to the question
    def get_author_answer(self):
        return Answer.objects.get(question=self, author=self.author)

    # return the absolute url for this question
    def get_absolute_url(self):
        return '/' + self.token + '/'

    # return the list of users that already answered to the question
    def already_answered(self):
        already_answered_users = []
        for answer in self.get_all_answers():
            already_answered_users.append(answer.author)
        return already_answered_users

    # return boolean according to the state of author answer
    def is_answer_published(self):
        if self.answer_date <= timezone.now():
            return True
        return False

    def author_answer(self):
        return 


class Answer(models.Model):
    """
        Define user answer to a question
    """
    question = models.ForeignKey(Question)
    text = models.TextField()
    author = models.ForeignKey(User, editable=False, null=True, blank=True)
    pub_date = models.DateTimeField('date published', auto_now=True)

    def __str__(self):
        return self.question.token + ' @' + self.author.username

