import xlrd
from django.contrib import admin

from . import models


@admin.register(models.TestObject)
class TestObjectAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.pk == None:
            obj.save()
            wb = xlrd.open_workbook(obj.file_of_test.storage.base_location + '/tests/' + form.files['file_of_test'].name)
            sheet = wb.sheet_by_index(0)
            sheet.cell_value(0, 0)
            instances = []
            for i in range(sheet.nrows):
                question = sheet.cell_value(i, 0)
                a = sheet.cell_value(i, 1)
                b = sheet.cell_value(i, 2)
                c = sheet.cell_value(i, 3)
                d = sheet.cell_value(i, 4)
                correct = sheet.cell_value(i, 5)
                instance = models.Test(
                    question=question,
                    optionA=a,
                    optionB=b,
                    optionC=c,
                    optionD=d,
                    correct_answer=correct,
                    test_object_id=obj.id
                )
                instance.save()

        return super(TestObjectAdmin, self).save_model(request, obj, form, change)


@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Listening)
class ListeningAdmin(admin.ModelAdmin):
    pass
