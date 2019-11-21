package com.SDClient;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.iid.FirebaseInstanceId;
import com.google.firebase.iid.InstanceIdResult;
import com.squareup.picasso.Picasso;

import java.net.URISyntaxException;

import io.socket.client.IO;
import io.socket.client.Socket;
import io.socket.emitter.Emitter;


public class MainActivity extends AppCompatActivity {
    private String token;
    private Socket mSocket;
    private String imageUrl = "";

    private String URL = "http://52.78.55.73:3000";

    {
        try {
            mSocket = IO.socket(URL);
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
    }
    TextView resident;
    Toast toast;
    ImageButton mic, mic_off, speak, speak_off, view, view_off, send;
    ImageView video;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        mSocket.connect();
        mSocket.on("Image",image);
        mSocket.on("DoorMsg", message);

        video = (ImageView) findViewById(R.id.video);
        resident = (TextView)findViewById(R.id.resident);

        /* ------이미지 버튼------ */
        mic = (ImageButton)findViewById(R.id.mic);
        mic_off = (ImageButton)findViewById(R.id.mic_off);
        speak = (ImageButton)findViewById(R.id.speak);
        speak_off = (ImageButton)findViewById(R.id.speak_off);
        view = (ImageButton)findViewById(R.id.view);
        view_off = (ImageButton)findViewById(R.id.view_off);
        send = (ImageButton)findViewById(R.id.setting);

        /* ------이미지 버튼 리스너------ */
        mic.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //mSocket.emit("MobileMsg","start");

                mic.setVisibility(View.GONE);
                mic_off.setVisibility(View.VISIBLE);
            }
        });

        mic_off.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //mSocket.emit("MobileMsg","start");
                mic_off.setVisibility(View.GONE);
                mic.setVisibility(View.VISIBLE);
            }
        });

        speak.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //mSocket.emit("MobileMsg","start");
                speak.setVisibility(View.GONE);
                speak_off.setVisibility(View.VISIBLE);
            }
        });

        speak_off.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                //mSocket.emit("MobileMsg","start");
                speak_off.setVisibility(View.GONE);
                speak.setVisibility(View.VISIBLE);
            }
        });

        view.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                mSocket.emit("MobileMsg","start");
                view.setVisibility(View.GONE);
                view_off.setVisibility(View.VISIBLE);
            }
        });

        view_off.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                mSocket.emit("MobileMsg","stop");
                view_off.setVisibility(View.GONE);
                view.setVisibility(View.VISIBLE);
            }
        });

        send.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View v) {
                mSocket.emit("Token",token);
            }
        });


        /*------Firebase 토큰 받기------*/
        FirebaseInstanceId.getInstance().getInstanceId()
                .addOnCompleteListener(new OnCompleteListener<InstanceIdResult>() {
                    @Override
                    public void onComplete(@NonNull Task<InstanceIdResult> task) {
                        token = task.getResult().getToken();
                    }
                });

    }

    private Emitter.Listener image = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    String receivedData = (String) args[0];


                    Glide.with(MainActivity.this)
                            .load(receivedData)
                            .centerCrop()
                            .dontAnimate()
                            .into(video);

                }
            });
        }
    };

    private Emitter.Listener message = new Emitter.Listener() {
        @Override
        public void call(final Object... args) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    String receivedData = (String) args[0];
                    resident.setText(receivedData);
                }
            });
        }
    };

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mSocket.disconnect();
    }
}
