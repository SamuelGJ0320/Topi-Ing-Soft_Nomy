from django.contrib import admin
from .models import Restaurant, searchahistory, Review

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(searchahistory)
admin.site.register(Review)