from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(dailyData)
admin.site.register(Counter)
admin.site.register(TestCounter)
