from django.contrib.auth.models import User
from django.db import models


class Test(models.Model):
    id = models.AutoField(primary_key=True)

    class ANSWERS(models.TextChoices):
        A = 'a'
        B = 'b'
        C = 'c'
        D = 'd'

    correct_answer = models.CharField(choices=ANSWERS.choices, max_length=10)
    question = models.CharField(max_length=100)
    optionA = models.CharField(max_length=100)
    optionB = models.CharField(max_length=100)
    optionC = models.CharField(max_length=100)
    optionD = models.CharField(max_length=100)
    test_object = models.ForeignKey('TestObject', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'[{self.id}]'


class TestObject(models.Model):
    qPaperTitle = models.CharField(max_length=100, blank=True, null=True)
    # questions = models.ForeignKey(QuestionDB, on_delete=models.CASCADE, blank=True, null=True)
    file_of_test = models.FileField(upload_to='tests', blank=True, null=True)

    def __str__(self):
        return self.qPaperTitle

    def total_of_questions(self):
        return len(Test.objects.filter(test_object=self.id))

    # def save(self, **kwargs):
    #     if self.pk == None:
    #         super(QuestionPaper, self).save(**kwargs)
    #         wb = xlrd.open_workbook(self.file_of_test.storage.base_location + '/' + self.file_of_test.name)
    #         sheet = wb.sheet_by_index(0)
    #         sheet.cell_value(0, 0)
    #         instances = []
    #         for i in range(sheet.nrows):
    #             question = sheet.cell_value(i, 0)
    #             a = sheet.cell_value(i, 1)
    #             b = sheet.cell_value(i, 2)
    #             c = sheet.cell_value(i, 3)
    #             d = sheet.cell_value(i, 4)
    #             correct = sheet.cell_value(i, 5)
    #             instance = QuestionDB(
    #                 question=question,
    #                 optionA=a,
    #                 optionB=b,
    #                 optionC=c,
    #                 optionD=d,
    #                 correct_answer=correct
    #             )
    #             instance.save()
    #             instances.append(instance)
    #         self.questions.set(instances)
    #
    #     return super(QuestionPaper, self).save(**kwargs)


class Results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_object = models.ForeignKey(TestObject, on_delete=models.SET_NULL, blank=True, null=True)
    score = models.CharField(max_length=25, null=True, blank=True)
    current_answers = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_level(self):
        result = float(self.score) / self.test_object.total_of_questions() * 100
        level = ''
        if result <= 40:
            level = 'Beginner'
        if 40 < result <= 75:
            level = 'Intermediate'
        if result > 75:
            level = 'Upper-intermediate'
        return level


class LevelsType(models.IntegerChoices):
    EASY = 1
    NORMAL = 2
    HARD = 3


class Listening(models.Model):
    audio_file = models.FileField(upload_to='audio_listening', blank=True, null=True)
    context = models.TextField()
    level = models.IntegerField(choices=LevelsType.choices, default=1)
    title = models.CharField(max_length=31)

    def __str__(self):
        return self.title


class ListeningResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.CharField(max_length=25, null=True, blank=True)
    listening_query = models.ForeignKey(Listening, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def get_level(self):
        result = float(self.score)
        level = ''
        if result <= 40:
            level = 'Beginner'
        if 40 < result <= 75:
            level = 'Intermediate'
        if result > 75:
            level = 'Upper-intermediate'
        return level
