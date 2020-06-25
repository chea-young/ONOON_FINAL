package com.example.xproject

import retrofit2.Call
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.POST

interface SignupService{
    @FormUrlEncoded
    @POST("/app_signup/")
    fun requestSignup(
        @Field("userid") userid:String,
        @Field("userpw") userpw:String,
        @Field("username") username:String

    ) : Call<Signup>
}



