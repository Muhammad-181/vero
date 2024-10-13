from django.contrib import admin
from .models import *

# Register your models here.

class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ( 'department', 'first_name',)
    list_filter = ( 'department', 'first_name',)



admin.site.register(StudentProfile, StudentProfileAdmin)
admin.site.register(Level)
admin.site.register(Department)
admin.site.register(Faculty)

    