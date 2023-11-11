import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    def test_future_question_not_published_recently(self):
        future_time = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=future_time)
        self.assertFalse(question.was_published_recently())

    def test_question_older_than_two_days_not_published_recently(self):
        time = timezone.now() - datetime.timedelta(days=2, seconds=1)
        question = Question(pub_date=time)
        self.assertFalse(question.was_published_recently())

    def test_recent_question_was_published_recently(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59)
        question = Question(pub_date=time)
        self.assertTrue(question.was_published_recently())

    def test_question_str_output(self):
        question_text = "some random text"
        question = Question.objects.create(question_text=question_text, pub_date=timezone.now())
        output = question.__str__()
        self.assertTrue(output == question_text)


def create_question(question_text, days):
    """
    Add a poll question that will be published the given number of days before or after today
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    def test_do_not_show_details_for_future_questions(self):
        """
        Do not show the details for questions that have a future publication date
        """
        create_question(question_text="Future poll", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [], )

    def test_show_details_for_past_questions(self):
        """
        Show questions with publication date in the past
        """
        question = create_question(question_text="Past poll", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question], )


class IndexViewTests(TestCase):

    def test_do_not_show_empty_question_list(self):
        """
        Display a message if there are no questions to display
        """
        response = self.client.get(reverse("polls:index"))
        self.assertTrue(response.status_code == 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_do_not_show_future_questions(self):
        """
        Do not show questions that have a future publication date
        """
        create_question(question_text="Future poll", days=1)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [], )

    def test_show_past_questions(self):
        """
        Show questions with publication date in the past
        """
        question = create_question(question_text="Past poll", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question], )

    def test_two_past_questions(self):
        """
        The index page can show multiple questions with publication dates in the past
        """
        question1 = create_question(question_text="Past poll 1", days=-1)
        question2 = create_question(question_text="Past poll 2", days=-2)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question1, question2], )

    def test_future_and_past_questions(self):
        """
        Do not show questions with a future publication date but do show questions
        with publication date in the past
        """
        create_question(question_text="Future poll", days=1)
        question = create_question(question_text="Past poll", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question], )
