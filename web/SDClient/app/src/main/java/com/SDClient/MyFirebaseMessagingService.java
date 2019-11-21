package com.SDClient;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class MyFirebaseMessagingService extends FirebaseMessagingService {
    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        super.onMessageReceived(remoteMessage);
        showNotification(remoteMessage.getNotification().getTitle(),remoteMessage.getNotification().getBody());

    }
    private void showNotification(String title, String message) {
        NotificationCompat.Builder notificationBuilder =
                new NotificationCompat.Builder(this, "MyNotifications")
                        .setSmallIcon(R.drawable.ic_launcher_background)
                        .setContentTitle(title)
                        .setContentText(message)
                        .setAutoCancel(true);

        NotificationManagerCompat Manager = NotificationManagerCompat.from(this);
        Manager.notify(999,notificationBuilder.build());

    }
}
