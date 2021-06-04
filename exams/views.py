import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import difflib

from . import models
from .models import Test


def test_list(request):
    tests = models.TestObject.objects.all()
    return render(request, 'exams/test-list.html', {'tests': tests, 'tag': 'exams'})


@login_required
def test_detail(request, pk):
    test = models.TestObject.objects.get(id=pk)
    if request.method == 'POST':
        data = request.POST
        tests = Test.objects.filter(test_object_id=test.id)

        score = 0
        answers = {}
        for i, ques in enumerate(tests):
            answers[str(i + 1)] = ques.correct_answer
            if ques.correct_answer == data['q' + str(i + 1)]:
                score += 1

        instance, _created = models.Results.objects.get_or_create(
            user_id=request.user.id,
            test_object=test,
            defaults={
                'score': score,
                'current_answers': json.dumps(answers),
            },
        )
        return render(request, 'exams/test-success.html', {'result': instance, 'tag': 'exams'})
    return render(request, 'exams/test-detail.html', {'test': test, 'tag': 'exams'})


def listening_list(request):
    all_listening = models.Listening.objects.all()
    return render(request, 'exams/listening-list.html', {'all_listening': all_listening, 'tag': 'exams'})


def similarity(s1, s2):
    normalized1 = s1.lower()
    normalized2 = s2.lower()
    matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
    return matcher.ratio()


@login_required
def listening_detail(request, pk):
    listening = models.Listening.objects.get(id=pk)
    if request.method == 'POST':
        context = request.POST['listening_content']

        score = round(similarity(context, listening.context) * 100, 2)

        instance, _created = models.ListeningResults.objects.get_or_create(
            user_id=request.user.id,
            listening_query_id=listening.id,
            defaults={
                'score': score,
            },
        )

        return render(request, 'exams/listening-result.html', {'result': instance, 'tag': 'exams'})
    return render(request, 'exams/listening-detail.html', {'listening': listening, 'tag': 'exams'})
