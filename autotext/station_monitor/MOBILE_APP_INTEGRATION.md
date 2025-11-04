# Mobile App Integration Guide

This guide explains how to integrate your custom iOS/Android app with the Station Monitoring System for push notifications.

## Overview

The system sends push notifications via HTTP POST requests to a webhook URL you configure. Your mobile app backend receives these notifications and forwards them to devices.

## Webhook Format

### Endpoint
```
POST https://your-app.com/api/notifications
```

### Headers
```
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY (optional)
```

### Payload Structure

#### Alert Notification
```json
{
  "title": "⚠️ Alert: Station 1 Out of Range",
  "message": "Alert: Station 1\n\nStatus: ABOVE maximum (125.50 > 120.0)\nCurrent Value: 125.50\nSafe Range: 50.0 - 120.0\nStation Phone: +1234567890\n\nAction Required: Contact technician to adjust readings.",
  "station": {
    "name": "Station 1",
    "phone": "+1234567890",
    "value": 125.50,
    "min": 50.0,
    "max": 120.0
  },
  "priority": "high",
  "type": "alert"
}
```

#### Test Notification
```json
{
  "title": "Test Notification",
  "message": "This is a test from Station Monitoring System",
  "type": "test",
  "priority": "normal"
}
```

### Response

Your endpoint should return:
- **200 OK** - Notification received successfully
- **401 Unauthorized** - Invalid API key
- **500 Error** - Server error

## Configuration Steps

### 1. In the Desktop App

1. Open the app
2. Go to **Settings** (⚙️ button)
3. Scroll to **Alert Notifications**
4. Check **📲 Push Notifications (Mobile App)**
5. Enter your webhook URL
6. (Optional) Enter API key for authentication
7. Click **💾 Save Settings**
8. Click **🧪 Test Push** to verify

### 2. In Your Mobile App Backend

Create an endpoint that:
1. Receives POST requests
2. Validates API key (if configured)
3. Parses the JSON payload
4. Sends push notification to registered devices
5. Returns 200 OK

#### Example Node.js/Express
```javascript
app.post('/api/notifications', async (req, res) => {
  // Validate API key
  const apiKey = req.headers.authorization?.replace('Bearer ', '');
  if (apiKey !== process.env.API_KEY) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  // Parse notification
  const { title, message, station, priority, type } = req.body;
  
  // Send to devices (using Firebase, OneSignal, etc.)
  await sendPushNotification({
    title,
    body: message,
    data: { station, type },
    priority
  });
  
  res.status(200).json({ success: true });
});
```

#### Example Python/Flask
```python
@app.route('/api/notifications', methods=['POST'])
def receive_notification():
    # Validate API key
    api_key = request.headers.get('Authorization', '').replace('Bearer ', '')
    if api_key != os.getenv('API_KEY'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    # Parse notification
    data = request.json
    title = data.get('title')
    message = data.get('message')
    station = data.get('station')
    priority = data.get('priority')
    
    # Send to devices
    send_push_notification(
        title=title,
        body=message,
        data={'station': station},
        priority=priority
    )
    
    return jsonify({'success': True}), 200
```

### 3. Push Notification Services

Choose a service to send notifications to devices:

#### Firebase Cloud Messaging (FCM)
- **Platforms:** iOS, Android, Web
- **Cost:** Free
- **Setup:** [firebase.google.com](https://firebase.google.com)

#### OneSignal
- **Platforms:** iOS, Android, Web
- **Cost:** Free tier available
- **Setup:** [onesignal.com](https://onesignal.com)

#### Apple Push Notification Service (APNs)
- **Platforms:** iOS only
- **Cost:** Free
- **Setup:** Apple Developer Account required

#### Custom Solution
- Use WebSockets or Server-Sent Events
- Direct HTTP/2 connection to APNs
- Firebase Admin SDK

## Mobile App Implementation

### iOS (Swift)

#### Register for Notifications
```swift
import UserNotifications

func registerForPushNotifications() {
    UNUserNotificationCenter.current()
        .requestAuthorization(options: [.alert, .sound, .badge]) { granted, _ in
            guard granted else { return }
            DispatchQueue.main.async {
                UIApplication.shared.registerForRemoteNotifications()
            }
        }
}
```

#### Handle Notification
```swift
func userNotificationCenter(
    _ center: UNUserNotificationCenter,
    didReceive response: UNNotificationResponse,
    withCompletionHandler completionHandler: @escaping () -> Void
) {
    let userInfo = response.notification.request.content.userInfo
    
    if let station = userInfo["station"] as? [String: Any] {
        // Handle station alert
        let stationName = station["name"] as? String
        let value = station["value"] as? Double
        // Navigate to station detail screen
    }
    
    completionHandler()
}
```

### Android (Kotlin)

#### Register for Notifications
```kotlin
import com.google.firebase.messaging.FirebaseMessaging

FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
    if (task.isSuccessful) {
        val token = task.result
        // Send token to your backend
        sendTokenToServer(token)
    }
}
```

#### Handle Notification
```kotlin
class MyFirebaseMessagingService : FirebaseMessagingService() {
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        remoteMessage.data.let { data ->
            val title = data["title"]
            val message = data["message"]
            val station = data["station"]
            
            // Show notification
            showNotification(title, message, station)
        }
    }
}
```

## Testing

### Test from Desktop App
1. Go to Settings → Alert Notifications
2. Configure push notification webhook
3. Click **🧪 Test Push**
4. Check your mobile app receives the test notification

### Test with curl
```bash
curl -X POST https://your-app.com/api/notifications \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "title": "Test Notification",
    "message": "Testing push notifications",
    "type": "test",
    "priority": "normal"
  }'
```

### Test with Postman
1. Create new POST request
2. URL: Your webhook URL
3. Headers: Content-Type: application/json
4. Headers: Authorization: Bearer YOUR_API_KEY
5. Body: Raw JSON (see payload structure above)
6. Send request

## Security Best Practices

### API Key
- Generate a strong, random API key
- Store securely (environment variables)
- Rotate regularly
- Never commit to version control

### HTTPS
- Always use HTTPS for webhook URL
- Validate SSL certificates
- Use TLS 1.2 or higher

### Rate Limiting
- Implement rate limiting on your endpoint
- Prevent abuse and DoS attacks
- Typical: 100 requests per minute

### Validation
- Validate all incoming data
- Check payload structure
- Sanitize inputs
- Log suspicious requests

## Troubleshooting

### Notifications Not Received

**Check Desktop App:**
- Settings → Alert Notifications → Push enabled?
- Webhook URL correct?
- Test button works?

**Check Backend:**
- Endpoint accessible?
- API key correct?
- Logs show incoming requests?
- Returns 200 OK?

**Check Mobile App:**
- Notifications permission granted?
- Device token registered?
- Push service configured?
- App in foreground/background?

### Test Failed

**Connection Error:**
- Check webhook URL is correct
- Ensure HTTPS (not HTTP)
- Verify firewall allows outbound connections
- Test URL in browser

**401 Unauthorized:**
- Check API key matches
- Verify Authorization header format
- Ensure Bearer prefix included

**Timeout:**
- Backend taking too long to respond
- Network connectivity issues
- Increase timeout in desktop app

## Advanced Features

### Custom Notification Sounds
```json
{
  "title": "Alert",
  "message": "Station out of range",
  "sound": "alert.wav",
  "badge": 1
}
```

### Action Buttons
```json
{
  "title": "Alert",
  "message": "Station out of range",
  "actions": [
    {"id": "call", "title": "Call Technician"},
    {"id": "view", "title": "View Details"}
  ]
}
```

### Rich Notifications
```json
{
  "title": "Alert",
  "message": "Station out of range",
  "image": "https://your-app.com/station-chart.png",
  "data": {
    "station_id": 123,
    "reading_id": 456
  }
}
```

## Example Mobile App Flow

1. **User opens app** → Registers for push notifications
2. **Device token generated** → Sent to your backend
3. **Backend stores token** → Associated with user account
4. **Desktop app detects alert** → Sends POST to webhook
5. **Backend receives notification** → Looks up user's devices
6. **Backend sends push** → Via FCM/APNs to devices
7. **User receives notification** → Taps to open app
8. **App opens to station detail** → Shows current readings

## Support

For help with mobile app integration:
- Check this guide
- Test with curl/Postman first
- Verify webhook URL is accessible
- Check backend logs
- Test with simple notification first

For push notification services:
- Firebase: [firebase.google.com/docs/cloud-messaging](https://firebase.google.com/docs/cloud-messaging)
- OneSignal: [documentation.onesignal.com](https://documentation.onesignal.com)
- APNs: [developer.apple.com/notifications](https://developer.apple.com/notifications)
