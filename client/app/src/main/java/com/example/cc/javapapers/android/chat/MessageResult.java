package com.example.cc.javapapers.android.chat;

import com.google.gson.annotations.SerializedName;

import java.util.List;

public class MessageResult {
    @SerializedName("messageSave")
    private List<String> messageSave;

    public MessageResult(List<String> messageSave) {
        this.messageSave = messageSave;
    }

    public MessageResult() {
        this.messageSave = messageSave;
    }

    // toString()을 Override 해주지 않으면 객체 주소값을 출력함
    @Override
    public String toString() {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < messageSave.size(); i++) {
            sb.append(messageSave.get(i));
            sb.append("|");
        }
        return "PostResult{" +
                "userId=" + sb.toString();
    }

    public List<String> getMessageSave() {
        return messageSave;
    }

    public void setMessageSave(List<String> messageSave) {
        this.messageSave = messageSave;
    }
}