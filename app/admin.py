from django.contrib import admin
from app import models
# Register your models here.


admin.site.register(models.CourseType)
admin.site.register(models.Course)
admin.site.register(models.Chapter)
admin.site.register(models.CourseCell)

