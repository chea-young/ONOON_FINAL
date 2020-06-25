package com.example.xproject

import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.http.*

interface OpendoorService{
    @Multipart
    @POST("/app_opendoor/")
    fun requestOpendoor(
        @Part imageFile : MultipartBody.Part
    ): Call<Addface>
}




