from django.db import models


class TestObjective(models.Model):
    test_id = models.CharField(max_length=50)
    # teacher_id = models.CharField(max_length=50)
    question_id = models.CharField(max_length=50)
    question = models.CharField(max_length=500)
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    ans = models.CharField(max_length=1)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.test_id} {self.question_id}"


class TestSubjective(models.Model):
    test_id = models.CharField(max_length=50)
    # teacher_id = models.CharField(max_length=50)
    question_id = models.IntegerField()
    question = models.CharField(max_length=500)
    marks = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.test_id}"


class TeacherTestJoin(models.Model):
    teacher_id = models.CharField(max_length=50)
    test_id = models.CharField(max_length=50)


class TestInformation(models.Model):
    test_id = models.CharField(max_length=50,primary_key=True)
    type = models.CharField(max_length=50)
    subject = models.CharField(max_length=500)
    topic = models.CharField(max_length=500)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    duration = models.IntegerField(default=30)
    neg_mark = models.IntegerField(default=0)
    password = models.CharField(max_length=20, )
    proctor_type = models.CharField(max_length=1, choices=[('0', 'Automatic Monitoring'), ('1', 'Live Monitoring')])

    def __str__(self):
        return f"{self.test_id}"