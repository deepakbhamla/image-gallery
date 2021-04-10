from django.contrib import admin
from .models import Tag, Gallery 
# Register your models here.


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("tag_name",)}

admin.site.register(Tag, TagAdmin)
admin.site.register(Gallery)
