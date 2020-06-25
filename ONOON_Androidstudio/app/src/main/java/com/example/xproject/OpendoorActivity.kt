package com.example.xproject

import android.app.Activity
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.ImageDecoder
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.gun0912.tedpermission.PermissionListener
import com.gun0912.tedpermission.TedPermission
import kotlinx.android.synthetic.main.activity_opendoor.*
import okhttp3.MediaType
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.File
import java.io.FileOutputStream
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.TimeUnit

class OpendoorActivity : AppCompatActivity() {
    val REQUEST_IMAGE_CAPTURE = 1
    lateinit var curPhotoPath: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_opendoor)
        if (intent.hasExtra("userid")) {
            checkid.text = intent.getStringExtra("userid")
        }
        /*if (intent.hasExtra("userpassword")){
            checkpass.text = intent.getStringExtra("userpassword")
        }*/
        exit_button.setOnClickListener {
            finish()
        }

        open_button.setOnClickListener {
            takeCapture()//사진촬영

        }
    }


    private fun takeCapture() {//카메라 실행
        //기본카메라 앱 실행
        Intent(MediaStore.ACTION_IMAGE_CAPTURE).also { takePictureIntent ->
            takePictureIntent.resolveActivity(packageManager)?.also {
                val photoFile: File? = try {
                    createImageFile() //이미지파일 생성하는 함수
                } catch (ex: IOException) {
                    null
                }
                photoFile?.also {
                    val photoURI: Uri = FileProvider.getUriForFile(
                        this,
                        "com.example.xproject.fileprovider",
                        it
                    )
                    takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI)
                    startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE)
                }

            }
        }

    }

    private fun createImageFile(): File? {//이미지파일 생성
        val timestamp: String = SimpleDateFormat("yyyyMMdd_HHmmss").format(Date())
        val storageDir: File? = getExternalFilesDir(Environment.DIRECTORY_PICTURES)
        return File.createTempFile("JPEG_${timestamp}_", ".jpg", storageDir)
            .apply { curPhotoPath = absolutePath }
    }

    //테드퍼미션 설정
    private fun setPermission() {
        val permission = object : PermissionListener {
            override fun onPermissionGranted() {//허용되었을경우 이거 수행
                Toast.makeText(this@OpendoorActivity, "권한이 허용되었습니다.", Toast.LENGTH_SHORT).show()
            }

            override fun onPermissionDenied(deniedPermissions: MutableList<String>?) {
                Toast.makeText(this@OpendoorActivity, "권한이 거부되었습니다.", Toast.LENGTH_SHORT).show()
            }
        }
        TedPermission.with(this)
            .setPermissionListener(permission)
            .setRationaleMessage("카메라 앱을 사용하시려면 권한을 허용해주세요.")
            .setDeniedMessage("권한을 거부하였습니다.")
            .setPermissions(
                android.Manifest.permission.WRITE_EXTERNAL_STORAGE,
                android.Manifest.permission.CAMERA
            )
            .check()

    }

    // 사진이 찍혔다는 신호가 오면
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == Activity.RESULT_OK) {
            val bitmap: Bitmap
            val file = File(curPhotoPath)
            if (Build.VERSION.SDK_INT < 28) {
                bitmap = MediaStore.Images.Media.getBitmap(contentResolver, Uri.fromFile(file))
                //frontface.setImageBitmap(bitmap)
            } else {
                val decode = ImageDecoder.createSource(
                    this.contentResolver,
                    Uri.fromFile(file)
                )
                bitmap = ImageDecoder.decodeBitmap(decode)
                //frontface.setImageBitmap(bitmap)
            }
            savePhoto(file, bitmap)
        }

    }

    private fun savePhoto(file: File, bitmap: Bitmap) {//갤러리에 저장
        val folderPath = Environment.getExternalStorageDirectory().absolutePath + "/Pictures/"
        val timestamp: String = SimpleDateFormat("yyyyMMdd_HHmmss").format(Date())
        val fileName = "${timestamp}.jpeg"
        val folder = File(folderPath)
        if (!folder.isDirectory) {//현재 해당경로에 폴더가 존재하는지
            folder.mkdir()
        }
        val out = FileOutputStream(folderPath + fileName)
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, out)
        //Toast.makeText(this, "사진이 앨범에 저장되었습니다", Toast.LENGTH_SHORT).show()
        sendPhoto(fileName, file)
    }

    private fun sendPhoto(fileName: String, file: File) {
        var requestBody: RequestBody = RequestBody.create(MediaType.parse("image/*"), file)
        var textId = checkid.text.toString()
        var body: MultipartBody.Part =
            MultipartBody.Part.createFormData("uploaded_file", textId + ".jpeg", requestBody)

        var gson: Gson = GsonBuilder()
            .setLenient()
            .create()

        var okHttpClient= OkHttpClient.Builder()
            .connectTimeout(8, TimeUnit.MINUTES)
            .readTimeout(20, TimeUnit.MINUTES)
            .writeTimeout(15, TimeUnit.SECONDS)
            .build()


        var retrofit = Retrofit.Builder()
            .baseUrl("http://192.168.0.4:8000")
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create(gson))
            .build()

        var opendoorService: OpendoorService = retrofit.create(OpendoorService::class.java)
        opendoorService.requestOpendoor(body).enqueue(object : Callback<Addface> {
            override fun onFailure(call: Call<Addface>, t: Throwable) {
                Log.d("레트로핏 결과1", t.message)
                var dialog = AlertDialog.Builder(this@OpendoorActivity)
                dialog.setTitle("User:"+textId)
                dialog.setMessage("얼굴인식에 실패하였습니다.")
                dialog.show()
            }

            override fun onResponse(call: Call<Addface>, response: Response<Addface>) {
                if (response?.isSuccessful) {
                    Log.d("레트로핏 결과2", "" + response?.body().toString())
                    var login = response.body()
                    Log.d("LOGIN", "msg : " + login?.msg)
                    Log.d("LOGIN", "code : " + login?.code)
                    //Toast.makeText(this@OpendoorActivity, "문이 열렸습니다.", Toast.LENGTH_SHORT).show()
                    var dialog = AlertDialog.Builder(this@OpendoorActivity)
                    dialog.setTitle("User:"+textId)
                    dialog.setMessage("문이 열렸습니다.")
                    dialog.show()

                } else {
                    var dialog = AlertDialog.Builder(this@OpendoorActivity)
                    dialog.setTitle("User:"+textId)
                    dialog.setMessage("얼굴인식에 실패하였습니다.")
                    dialog.show()
                }
            }
        })
    }
}