from django.contrib import admin
from .models import Link

# Register your models here.
admin.autodiscover()

class UserAdmin(admin.ModelAdmin):
    list_display=('user','item','date',)
    list_filter=['date']

admin.site.register(Link,UserAdmin)
