from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Addresses, Pictures, LoginPicture
from .serializers import AddressesSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
import json

from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password


import sys
sys.path.insert(0, 'C:/Users/w1004/Desktop/xproject/xproject/ml')
import face_recog_3


from socket import *
import threading
import time

@csrf_exempt 
def address_list(request): 
    if request.method == 'GET': 
        query_set = Addresses.objects.all() 
        serializer = AddressesSerializer(query_set, many=True) 
        return JsonResponse(serializer.data, safe=False) 
    
    elif request.method == 'POST': 
        data = JSONParser().parse(request) 
        serializer = AddressesSerializer(data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data, status=201) 
        return JsonResponse(serializer.errors, status=400) 
        
@csrf_exempt 
def address(request, pk): 
    obj = Addresses.objects.get(pk=pk) 
    if request.method == 'GET': 
        serializer = AddressesSerializer(obj) 
        return JsonResponse(serializer.data, safe=False) 
        
    elif request.method == 'PUT': 
        data = JSONParser().parse(request) 
        serializer = AddressesSerializer(obj, data=data) 
        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data, status=201) 
        return JsonResponse(serializer.errors, status=400) 
    
    elif request.method == 'DELETE': 
        obj.delete() 
        return HttpResponse(status=204) 
        
@csrf_exempt 
def login(request): 
    if request.method == 'POST': 
        print("request "+ str(request)) 
        print("body "+ str(request.body)) 
        userid = request.POST.get("userid", "") 
        userpw = request.POST.get("userpw", "") 
        login_result = authenticate(username=userid, password=userpw)
        print("userid = " + userid + " result = " + str(login_result))
    print("userid = " + userid + " result = " + str(login_result)) 
    if login_result: 
        return HttpResponse(status=200) 
    else: 
        return render(request, "addresses/login.html", status=401)
    return render(request, "addresses/login.html")


@csrf_exempt
def app_login(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))
        id = request.POST.get('userid', '')
        pw = request.POST.get('userpw', '')
        print("id = " + id + " pw = " + pw)
        ##디비에서 id,pw 가져와서 -> 확인=result
        myuser = Addresses.objects.filter(userid=id, userpw=pw)
        print(myuser)
        if myuser:
            print("로그인 성공!")
            return JsonResponse({'code': '0000', 'msg': '로그인성공입니다.'}, status=200)
        else :
            print("로그인 실패")

@csrf_exempt
def app_signup(request):
    if request.method == 'POST':
        print("리퀘스트 로그" + str(request.body))
        id = request.POST.get('userid', '')
        pw = request.POST.get('userpw', '')
        username = request.POST.get('username', '')
        print("id = " + id + " pw = " + pw + " name = " + username)
        myuser = Addresses.objects.filter(userid=id)       
        if myuser:
            print("중복!")
        else:
            # db 저장
            form = Addresses(userid=id, userpw=pw,name=username)
            form.save()
            print("성공")
            return JsonResponse({'code': '1001', 'msg': '회원가입성공입니다.'}, status=200)

@csrf_exempt
def app_app_addface(request):
    if request.method == 'POST':
        photo = request.FILES.get('uploaded_file')
        photo_name = photo.name[:-7]
        if('_1' in photo.name):
            print("_1")
            form = Pictures(userid=photo_name, first_picture = photo)
            form.save()
        elif('_2' in photo.name):
            print("_2")
            user = Pictures.objects.get(userid=photo_name)
            user.second_picture = photo
            user.save()
        elif('_3' in photo.name):
            print("_3")
            user = Pictures.objects.get(userid=photo_name)
            user.third_picture = photo
            user.save()
        return JsonResponse({'code': '0000', 'msg': '사진받았습니다.'}, status=200)

@csrf_exempt
def app_app_opendoor(request):

    if request.method == 'POST':
        photo = request.FILES.get('uploaded_file')
        photo_name = photo.name[:-5]
        #print("photo = "+photo_name)
        form = LoginPicture(userid=photo_name, login_picture = photo)
        form.save()
        #print(photo_name)
        lock_state, unlock_name = face_recog_3.run(face_recog_3.trains(), photo.file)
        print((lock_state, unlock_name))

        #추가
        user = Pictures.objects.get(userid=photo_name)
        user_lock_state, user_unlock_name = face_recog_3.run(face_recog_3.trains(), user.first_picture)
        print((user_lock_state, user_unlock_name))
        
        if(lock_state == "unlock" and user_lock_state == "unlock" and unlock_name == user_unlock_name):
            sys.path.insert(1, 'C:/Users/w1004/Desktop/xproject/xproject/')
            import server_close
            server_close.opendoor()
            return JsonResponse({'code': '0000', 'msg': '사진받았습니다.'}, status=200)

def login_page(request): 
    return render(request, "addresses/login.html")
