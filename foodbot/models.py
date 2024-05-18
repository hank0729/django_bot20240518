from django.db import models
import uuid

class UserMessage(models.Model):
    line_id = models.CharField(max_length=50)
    message_text = models.TextField()

    def __str__(self):
        return self.line_id

class First(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex)
    lineid = models.TextField()
    q1 = models.TextField()
    q2 = models.TextField()
    q3 = models.TextField()
    q4 = models.TextField()
    q5 = models.TextField()
    q6 = models.TextField()
    q7 = models.TextField()
    q8 = models.TextField()
    q9 = models.TextField()
    q10 = models.TextField()
    q11 = models.TextField()
    q12 = models.TextField()
    q13 = models.TextField()
    q14 = models.TextField()
    q15 = models.TextField()
    q16 = models.TextField()
    q17 = models.TextField()
    q18 = models.TextField()
    q19 = models.TextField()
    q20 = models.TextField()
    q21 = models.TextField()
    q22 = models.TextField()
    q23 = models.TextField()
    q24 = models.TextField()
    q25 = models.TextField()
    q26 = models.TextField()
    q27 = models.TextField()

class Main(models.Model):
    lineid = models.CharField(max_length=255, unique=True)
    days = models.IntegerField(default=0)
    first = models.ForeignKey('First', on_delete=models.CASCADE)
    first_key = models.TextField()
    seven = models.ForeignKey('Seven', on_delete=models.CASCADE)
    seven_key = models.TextField()
    month = models.ForeignKey('Month', on_delete=models.CASCADE)
    month_key = models.TextField()
    twomonth = models.ForeignKey('TwoMonth', on_delete=models.CASCADE)
    twomonth_key = models.TextField()
    threemonth = models.ForeignKey('ThreeMonth', on_delete=models.CASCADE)
    threemonth_key = models.TextField()

    def __str__(self):
        return self.lineid


class Seven(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex)
    lineid = models.TextField()
    q1 = models.TextField()
    q2 = models.TextField()
    q3 = models.TextField()
    q4 = models.TextField()
    q5 = models.TextField()
    q6 = models.TextField()
    q7 = models.TextField()

class Month(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex)
    lineid = models.TextField()
    q1 = models.TextField()
    q2 = models.TextField()
    q3 = models.TextField()
    q4 = models.TextField()
    q5 = models.TextField()
    q6 = models.TextField()
    q7 = models.TextField()
    q8 = models.TextField()
    q9 = models.TextField()
    q10 = models.TextField()

class TwoMonth(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex)
    lineid = models.TextField()
    q1 = models.TextField()
    q2 = models.TextField()
    q3 = models.TextField()
    q4 = models.TextField()
    q5 = models.TextField()
    q6 = models.TextField()
    q7 = models.TextField()
    q8 = models.TextField()
    q9 = models.TextField()
    q10 = models.TextField()

class ThreeMonth(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex)
    lineid = models.TextField()
    q1 = models.TextField()
    q2 = models.TextField()
    q3 = models.TextField()
    q4 = models.TextField()
    q5 = models.TextField()
    q6 = models.TextField()
    q7 = models.TextField()
    q8 = models.TextField()
    q9 = models.TextField()
    q10 = models.TextField()
    q11 = models.TextField()
    q12 = models.TextField()
    q13 = models.TextField()
    q14 = models.TextField()
    q15 = models.TextField()
