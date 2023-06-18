package com.example.cc.javapapers.android.chat;

import okhttp3.MultipartBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;
import retrofit2.http.Query;
import retrofit2.http.QueryMap;

public interface RetrofitService {
    @GET("/getMessages")
    Call<MessageResult> getPosts();

    @GET("/addMessage")
    Call<AddMessage> getAddMessageGets(
        @Query("name") String name,
        @Query("message") String message
    );

    @GET("/command")
    Call<ResponseBody> getCommandResult(
        @Query("command") String command
    );
}
