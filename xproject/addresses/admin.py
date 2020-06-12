from django.contrib import admin
from .models import Addresses, Pictures, LoginPicture   #같은 경로의 models.py에서 User라는 클래스를 임포트한다.

# Register your models here.

class UserAdmin(admin.ModelAdmin) :
    list_display = ('userid', 'userpw', 'name')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['userid','first_picture','second_picture', 'third_picture']

class LoginPhotoAdmin(admin.ModelAdmin):
    list_display = ['userid','login_picture']

admin.site.register(Addresses, UserAdmin) 
admin.site.register(Pictures, PhotoAdmin)
admin.site.register(LoginPicture, LoginPhotoAdmin)
# Register your models here.
