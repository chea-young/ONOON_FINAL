package com.example.xproject

import okhttp3.MultipartBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.http.*

interface AddfaceService{
    @Multipart
    @POST("/app_addface/")
    fun requestAddface(
        @Part imageFile : MultipartBody.Part
    ): Call<Addface>
}




