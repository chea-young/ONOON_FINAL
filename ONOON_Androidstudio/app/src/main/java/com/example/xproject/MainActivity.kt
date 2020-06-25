package com.example.xproject

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import kotlinx.android.synthetic.main.activity_main.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        var retrofit = Retrofit.Builder()
                .baseUrl("http://192.168.0.4:8000")
                .addConverterFactory(GsonConverterFactory.create())
                .build()
        // baseUrl은 내 local 주소
        var loginService: LoginService = retrofit.create(LoginService::class.java)

        // 로그인하는 경우
        button.setOnClickListener {
            var textId = editTextTextPersonName.text.toString()
            var textPw = editTextTextPassword.text.toString()
            val intent = Intent(this, OpendoorActivity::class.java)
            loginService.requestLogin(textId, textPw).enqueue(object : Callback<Login> {
                    override fun onFailure(call: Call<Login>, t: Throwable) {
                        Log.e("DEBUG", t.message)
                        var dialog = AlertDialog.Builder(this@MainActivity)
                        dialog.setTitle("실패")
                        dialog.setMessage("통신에 실패했습니다..")
                        dialog.show()
                    }
                    override fun onResponse(call: Call<Login>, response: Response<Login>) {
                        if (response?.isSuccessful) {
                            var login = response.body()
                            Log.d("LOGIN", "msg : " + login?.msg)
                            Log.d("LOGIN", "code : " + login?.code)
                            var dialog = AlertDialog.Builder(this@MainActivity)
                            Toast.makeText(this@MainActivity, "로그인이 되었습니다.", Toast.LENGTH_SHORT)
                                .show()
                            // 로그인 시 다음 창으로 이동
                            intent.putExtra("userid", textId)
                            //intent.putExtra("userpassword", textPw)
                            startActivity(intent)
                            finish()
                        }else{
                            // id또는 password가 틀렸을 시 로그인이 실패되기 때문에 창 이동이 없는 경우
                            Toast.makeText(this@MainActivity, "로그인이 실패하셨습니다.", Toast.LENGTH_SHORT).show()
                        }
                    }
            })
        }
        //회원가입 화면으로 가는 경우
        signup_button.setOnClickListener {
            val intent = Intent(this, SignupActivity::class.java)
            startActivity(intent)
            finish()
        }
    }
}