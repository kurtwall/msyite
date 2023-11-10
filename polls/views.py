from django.http import HttpResponse


def index(request):
    return HttpResponse("This is the polls index")


def detail(request, question_id):
    response = "You're looking at question %s."
    return HttpResponse(response % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    response = "You're voting on question %s."
    return HttpResponse(response % question_id)

