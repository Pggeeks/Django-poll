from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Question_Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=User)
    question = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        overiding the save method to count the number of objects
        a user is saving if it reaches 5 the object will not be saved
        @pggeeks/Parth gujral
        """
        if Question_Model.objects.filter(user=self.user).count() <= 4:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.question


class Option_Model(models.Model):
    poll = models.ForeignKey(Question_Model, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    option_1_count = models.IntegerField(default=0)
    option_2_count = models.IntegerField(default=0)
    option_3_count = models.IntegerField(default=0)
    option_4_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.poll.question[:10]} Options"

    def Total_Votes(self):
        return (
            self.option_1_count
            + self.option_2_count
            + self.option_3_count
            + self.option_4_count
        )


class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Question_Model, on_delete=models.CASCADE)
