import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Create a poll question
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Return true if poll published in the past day
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()


class Choice(models.Model):
    """
    Create choices for the associated poll question
    """
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
