package com.example.xproject

data class Signup(
    //code, msg는 서버 앱에서 view.py의 key 값과 같아야 한다.
    val code: String,
    val msg: String
)