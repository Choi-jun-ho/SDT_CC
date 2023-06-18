package com.example.cc.javapapers.android.chat;

import static java.lang.Thread.sleep;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.database.DataSetObserver;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.text.Layout;
import android.util.Log;
import android.view.KeyEvent;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnKeyListener;
import android.view.inputmethod.InputMethodManager;
import android.widget.AbsListView;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.widget.Toolbar;
import androidx.appcompat.app.AppCompatActivity;

import com.example.cc.R;

import java.io.InputStream;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Enumeration;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;


import okhttp3.MultipartBody;
import okhttp3.OkHttpClient;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ChatBubbleActivity extends AppCompatActivity {
    private static final String TAG = "ChatActivity";

    private ChatArrayAdapter chatArrayAdapter;
    private ListView listView;
    private EditText chatEditText;
    private Button buttonSend;
    Layout activity_chat;

    Intent intent;
    private boolean side = false;

    Retrofit retrofit;


    int messageCount = 0;

    Timer messageTimer;
    TimerTask TT;
    boolean isMessageRespon = false;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent i = getIntent();
        setContentView(R.layout.activity_chat);

        Toolbar toolbar = findViewById (R.id.toolbar2);
        setSupportActionBar (toolbar);
        ActionBar actionBar = getSupportActionBar ();
        actionBar.setDisplayHomeAsUpEnabled (true);


        String ip = "192.168.0.21";
        OkHttpClient okHttpClient = new OkHttpClient.Builder()
                .connectTimeout(60, TimeUnit.SECONDS)
                .readTimeout(60, TimeUnit.SECONDS)
                .writeTimeout(60, TimeUnit.SECONDS)
                .build();

        retrofit =  new Retrofit.Builder()
                .baseUrl("http://" + ip + ":5000/")
                .client(okHttpClient)
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        messageTimer = new Timer();

        buttonSend = (Button) findViewById(R.id.buttonSend);

        listView = (ListView) findViewById(R.id.listView1);

        chatArrayAdapter = new ChatArrayAdapter(getApplicationContext(), R.layout.activity_chat_singlemessage);
        listView.setAdapter(chatArrayAdapter);

        chatEditText = (EditText) findViewById(R.id.chatText);

        chatEditText.setOnKeyListener(new OnKeyListener() {
            public boolean onKey(View v, int keyCode, KeyEvent event) {
                if ((event.getAction() == KeyEvent.ACTION_DOWN) && (keyCode == KeyEvent.KEYCODE_ENTER)) {
                    return sendChatMessage();
                }
                return false;
            }
        });

        buttonSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View arg0) {
                sendChatMessage();
                closeKeyboard();
            }
        });

        listView.setTranscriptMode(AbsListView.TRANSCRIPT_MODE_ALWAYS_SCROLL);
        listView.setAdapter(chatArrayAdapter);

        //to scroll the list view to bottom on data change
        chatArrayAdapter.registerDataSetObserver(new DataSetObserver() {
            @Override
            public void onChanged() {
                super.onChanged();
                listView.setSelection(chatArrayAdapter.getCount() - 1);
            }
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        new Thread(new Runnable() {
            @Override
            public void run() {
                while (true) {

                    try {
                        sleep(300);
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                    if (isMessageRespon == false) {
                        RetrofitService retrofitService = retrofit.create(RetrofitService.class);
                        isMessageRespon = true;
                        Call<MessageResult> call = retrofitService.getPosts();
                        call.enqueue(new Callback<MessageResult>() {
                            @Override
                            public void onResponse(Call<MessageResult> call, Response<MessageResult> response) {

                                if(response.isSuccessful()){
                                    MessageResult result = response.body();
                                    List<String> messageSave = result.getMessageSave();

                                    for (int i = messageCount; i < messageSave.size(); i++) {
                                        String[] messageInfo = messageSave.get(i).split(",");
                                        sendChatMessage(messageInfo[0], messageInfo[1], messageInfo[2], false, null, i*10);
                                        if (messageInfo[1].startsWith("/")) {
                                            getImage(messageInfo[1], messageInfo[2], i * 10 + 5);
                                        }
                                    }
                                    messageCount = messageSave.size();
//                                    Log.d(TAG, "onResponse: 성공, 결과\n"+ result.toString());
                                } else {
                                    Log.d(TAG, "onResponse: 실패");
                                }
                                isMessageRespon = false;
                            }

                            @Override
                            public void onFailure(Call<MessageResult> call, Throwable t) {
                                Log.d(TAG, "onFailure:" + t.getMessage());
                            }
                        });

                    }
                }

            }
        }).start();

    }

    @Override
    protected void onStop() {
        super.onStop();

    }

    @SuppressLint("NonConstantResourceId")
    @Override
    public boolean onOptionsItemSelected( MenuItem item) {
        switch (item.getItemId ()) {
            case android.R.id.home:
                finish ();
                return true;
            default:
                return super.onOptionsItemSelected (item);
        }
    }

    private boolean sendChatMessage(){

        String message = chatEditText.getText().toString();

        if (message.equals(""))
            return false;

        RetrofitService retrofitService2 = retrofit.create(RetrofitService.class);
        Call<AddMessage> call2 = retrofitService2.getAddMessageGets("준호", message);
        call2.enqueue(new Callback<AddMessage>() {
            @Override
            public void onResponse(Call<AddMessage> call, Response<AddMessage> response) {
                if (response.isSuccessful()) {
                    Log.d(TAG, "AAAonResponse: 성공, 결과\n앱에서 전송 성공");
                } else {
                    Log.d(TAG, "AAAonResponse: 실패");
                }
            }

            @Override
            public void onFailure(Call<AddMessage> call, Throwable t) {
                Log.d(TAG, "AAonFailure:" + chatEditText.getText().toString() + t.getMessage());
            }
                });
        chatEditText.setText("");
        return true;
    }

    private boolean getImage(String message, String time, int i) {
        RetrofitService retrofitService3 = retrofit.create(RetrofitService.class);
        Log.d("getImage", "image comand msg : " + message);
        Call<ResponseBody> call3 = retrofitService3.getCommandResult(message);
        call3.enqueue(new Callback<ResponseBody>() {
            @Override
            public void onResponse(Call<ResponseBody> call, Response<ResponseBody> response) {
                if (response.isSuccessful()) {
                    InputStream is = response.body().byteStream();
                    Bitmap bitmap = BitmapFactory.decodeStream(is);
                    sendChatMessage("ProjectManagerBot", "", time, true, bitmap, i);
                    Log.d(TAG, "image onResponse: 성공, 결과\ncommand 성공");
                } else {
                    Log.d(TAG, "image onResponse: 실패");
                }
            }

            @Override
            public void onFailure(Call<ResponseBody> call, Throwable t) {
                Log.d(TAG, "image onFailure:" + t.getMessage());
            }
        });

        return true;
    }

    private boolean sendChatMessage(String user, String message, String time, boolean isImage, Bitmap bitmap, int i) {
        side = true;
        if (user.equals("준호"))
            side = false;
        chatArrayAdapter.add(new ChatMessage(side, user, message, time, isImage, bitmap, i));
        return true;
    }

    private void closeKeyboard() {
        View view = this.getCurrentFocus();
        if (view != null) {
            InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
            imm.hideSoftInputFromWindow(view.getWindowToken(), 0);
        }
    }

    public static String getLocalIpAddress() {
        try {
            for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements();) {
                NetworkInterface intf = en.nextElement();
                for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();) {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress() && inetAddress instanceof Inet4Address) {
                        return inetAddress.getHostAddress();
                    }
                }
            }
        } catch (SocketException ex) {
            ex.printStackTrace();
        }
        return null;
    }


}