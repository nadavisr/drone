package com.example.administrator.ffmpeg;

import android.graphics.Bitmap;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;

import java.nio.ByteBuffer;

public class MainActivity extends AppCompatActivity {

    TextView t;
    FFmpeg m_ffmpeg;
    ImageView view;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //t = findViewById(R.id.imageView);
        view = findViewById(R.id.imageView);

        ImageProvider imageProvider = new ImageProvider() {
            @Override
            public void frameReady(final byte[] rgb, final int width, final int hight) {
                try {
                    Log.i("Drone", "MainActivity received image");

//                    Bitmap bitmap = BitmapFactory.decodeByteArray(rgb, 0, rgb.length);
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            Bitmap bm = Bitmap.createBitmap(width, hight, Bitmap.Config.ARGB_8888);
                            bm.copyPixelsFromBuffer(ByteBuffer.wrap(rgb));
                            view.setImageBitmap(bm);
                            view.invalidate();
                        }
                    });
                }
                catch (Exception e)
                {
                    Log.i("Drone",e.toString());
                }
            }
        };

        FFmpeg m_ffmpeg = FFmpeg.getInstance(this);
        m_ffmpeg.setImageProvider(imageProvider);
        String version = "-version";
        //String[] cmd = new String[]{ "-i", "-", "-f","image2pipe", "-vcodec", "rawvideo", "-pix_fmt", "rgb24", "-"};

        ///storage/emulated/0/Download/Output.mp4
       // String[] cmd =new String[]{"-i","/storage/emulated/0/Download/bug.mov","/storage/emulated/0/Download/Output.mp4"};
         String[] cmd =new String[]{"-i", "-", "-f", "image2pipe", "-pix_fmt", "bgr32", "-vcodec", "rawvideo", "-"};
        try {
            // to execute "ffmpeg -version" command you just need to pass "-version"
            m_ffmpeg.execute(cmd, new ExecuteBinaryResponseHandler()
            {

                @Override
                public void onStart() { }

                @Override
                public void onProgress(String message){
                    //t.setText(message);
                }

                @Override
                public void onFailure(String message){
                //    t.setText(message);
                }

                @Override
                public void onSuccess(String message){
                //    t.setText(message);
                }

                @Override
                public void onFinish() { }
            });
        }
        catch (FFmpegCommandAlreadyRunningException e)
        {
            // Handle if FFmpeg is already running
            System.out.println("Handle if FFmpeg is already running");
        }

  /*


        OutputStream stdin = process.getOutputStream(); // <- Eh?
        InputStream stdout = process.getInputStream();

        BufferedReader reader = new BufferedReader(new InputStreamReader(stdout));
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(stdin));

*/

    }
}
