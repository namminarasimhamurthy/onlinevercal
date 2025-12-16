from django.contrib import admin
from .models import RegisterUser
from .models import Question

admin.site.register(RegisterUser)
admin.site.register(Question)