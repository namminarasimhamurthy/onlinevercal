from django.db import models

class RegisterUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Question(models.Model):
    COURSE_CHOICES = [
        ('python', 'Python'),
        ('webdev', 'Web Development'),
        ('datasci', 'Data Science'),
    ]

    course = models.CharField(max_length=20, choices=COURSE_CHOICES)
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course} - {self.question_text[:50]}"
