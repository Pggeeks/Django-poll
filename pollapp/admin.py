from django.contrib import admin
from .models import Option_Model, Question_Model, Voter
# Register your models here.
admin.site.register(Question_Model)
admin.site.register(Option_Model)
admin.site.register(Voter)
