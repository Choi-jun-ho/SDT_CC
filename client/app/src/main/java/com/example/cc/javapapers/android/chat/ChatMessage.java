package com.example.cc.javapapers.android.chat;

import android.graphics.Bitmap;

public class ChatMessage {
	public boolean left;
	public String message;
	public String time;
	public String user;
	public int key;
	public Bitmap bitmap;
	public boolean isImage;
	public ChatMessage(boolean left, String user, String message, String time, boolean isImage, Bitmap bitmap, int key) {
		super();
		this.left = left;
		this.user = user;
		this.message = message;
		this.time = time;
		this.isImage = isImage;
		this.bitmap = bitmap;
		this.key = key;
	}
}