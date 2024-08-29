from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from discussions.models import Student

class Request(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=60)
    pub_date = models.DateTimeField(blank=False, default=now)

    def __str__(self) -> str:
        return self.file_name


class Contribution(models.Model):
    contributor = models.ForeignKey(Student, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    file = models.FileField()
    pub_date = models.DateTimeField(blank=False, default=now)

    def __str__(self) -> str:
        return self.request.file_name
