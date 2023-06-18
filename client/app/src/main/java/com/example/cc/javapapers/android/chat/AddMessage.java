package com.example.cc.javapapers.android.chat;

import androidx.constraintlayout.motion.utils.ViewSpline;

import com.google.gson.annotations.SerializedName;

import java.util.List;

public class AddMessage {
    @SerializedName("result")
    private String result;

    public AddMessage(String result) {
        this.result = result;
    }

    // toString()을 Override 해주지 않으면 객체 주소값을 출력함
    @Override
    public String toString() {
        return this.result;
    }

    public String getAddMessageInfo() {
        return result;
    }
}
