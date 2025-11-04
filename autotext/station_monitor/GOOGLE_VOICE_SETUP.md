# Google Voice Setup Guide

Complete guide for using Google Voice to receive AND send SMS alerts - completely FREE!

## Overview

Google Voice provides:
- **FREE phone number**
- **FREE incoming SMS**
- **FREE outgoing SMS**
- **Automatic message receiving**
- **No monthly fees**

Perfect for personal use and testing!

## Part 1: Get Google Voice

### Step 1: Sign Up

1. Go to [voice.google.com](https://voice.google.com)
2. Sign in with your Google account
3. Click "Get Google Voice"
4. Choose a phone number (search by area code or city)
5. Verify with your existing phone number
6. Complete setup

### Step 2: Test Your Number

1. Send a test SMS to your new Google Voice number
2. Check that it appears in voice.google.com
3. Reply to confirm it works

## Part 2: Configure for Receiving Messages

### Step 1: Create App Password

**Why?** Google requires App Passwords for third-party apps.

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Go to **App Passwords**
4. Select app: **Mail**
5. Select device: **Other** (enter "Station Monitor")
6. Click **Generate**
7. Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)
8. **Save this password** - you'll need it in the app

### Step 2: Install Library

Open Command Prompt and run:
```bash
pip install googlevoice
```

### Step 3: Configure in App

1. Open Station Monitoring System
2. Go to **Settings** (⚙️ button)
3. Under **SMS Reception Method**:
   - Select: **Google Voice**
   - Enter your Gmail address (e.g., `your@gmail.com`)
   - Enter your App Password (the 16-character one)
   - Set check interval: **60** seconds (recommended)
4. Click **💾 Save Settings**

### Step 4: Start Receiver

1. Still in Settings
2. Look for **● Stopped** status at top
3. Click **▶ Start Receiver** button
4. Should change to **● Running** (green)
5. App will now check for messages every 60 seconds

### Step 5: Test It!

1. Send a test message to your Google Voice number:
   ```
   Station 1 - 56.893
   ```
2. Wait up to 60 seconds
3. Check Dashboard - reading should appear automatically!
4. Check History to see the received message

## Part 3: Configure for Sending Alerts

### Step 1: Configure SMS Notifications

1. Go to **Settings** → **Alert Notifications**
2. Check **📱 SMS Notifications**
3. Select Provider: **google_voice**
4. Enter your Gmail address
5. Enter your App Password (same as above)
6. Enter recipient numbers (comma-separated):
   ```
   +1234567890, +0987654321
   ```
7. Click **💾 Save Settings**

### Step 2: Test Alerts

1. Go to **Manual Entry**
2. Select a station
3. Enter a value **outside** the safe range
4. Click **Submit Reading**
5. You should receive an SMS alert!

## Complete Setup Checklist

- [ ] Got Google Voice number
- [ ] Tested sending/receiving on voice.google.com
- [ ] Enabled 2-Step Verification
- [ ] Created App Password
- [ ] Installed googlevoice library
- [ ] Configured receiving in Settings
- [ ] Started receiver (green status)
- [ ] Tested receiving a message
- [ ] Configured SMS notifications
- [ ] Tested sending an alert

## How It Works

### Receiving Messages

```
Technician → Google Voice Number
                ↓
        Google Voice Server
                ↓
    App polls every 60 seconds
                ↓
        Finds new message
                ↓
        Parses value
                ↓
        Saves to database
                ↓
        Updates dashboard
                ↓
    Sends alerts if out of range
```

### Sending Alerts

```
Reading out of range detected
            ↓
    Notification system triggered
            ↓
    Google Voice API called
            ↓
    SMS sent to recipients
            ↓
    You receive alert on phone
```

## Troubleshooting

### Receiver Won't Start

**Error: "Google Voice library not installed"**
```bash
pip install googlevoice
```

**Error: "Login failed"**
- Check email address is correct
- Use App Password, not regular password
- Make sure 2-Step Verification is enabled
- Try generating a new App Password

**Status stays "Stopped"**
- Check credentials in Settings
- Click "Start Receiver" button
- Check console for error messages

### Messages Not Received

**Check:**
1. Receiver status is **● Running** (green)
2. Message was sent to correct Google Voice number
3. Message appears on voice.google.com
4. Station phone number matches sender
5. Message contains a numeric value

**Wait:**
- App checks every 60 seconds
- May take up to 1 minute to appear

**Test:**
- Send message: "Station 1 - 56.893"
- Wait 60 seconds
- Check Dashboard

### Alerts Not Sent

**Check:**
1. SMS Notifications enabled in Settings
2. Provider set to "google_voice"
3. Credentials entered correctly
4. Recipient numbers in correct format (+1234567890)
5. Reading is actually out of range

**Test:**
- Submit out-of-range reading
- Check console for errors
- Verify on voice.google.com that message was sent

### "Unknown phone number"

**Problem:** Message received but not processed

**Solution:**
1. Go to **Manage Stations**
2. Check station phone number matches sender
3. Phone numbers must match exactly
4. Format: +1234567890 (E.164 format)

### Rate Limiting

**Problem:** Too many messages

**Solution:**
- Google Voice has fair use limits
- Don't exceed ~100 messages/day
- For high volume, use Twilio instead

## Best Practices

### Phone Number Format

**Correct:**
- `+1234567890` (E.164 format)
- Include country code
- No spaces, dashes, or parentheses

**Wrong:**
- `(123) 456-7890`
- `123-456-7890`
- `1234567890` (missing +)

### Check Interval

**Recommended:** 60 seconds
- Good balance of responsiveness and API usage
- Not too frequent to trigger rate limits
- Not too slow to miss urgent alerts

**Faster:** 30 seconds
- More responsive
- Higher API usage
- May hit rate limits

**Slower:** 120 seconds
- Lower API usage
- Less responsive
- Good for non-urgent monitoring

### Security

**Protect Your Credentials:**
- Never share App Password
- Don't commit config.json to version control
- Rotate App Password periodically
- Use dedicated Google account (optional)

**Dedicated Account:**
- Create separate Gmail for monitoring
- Keeps personal email separate
- Easier to manage
- Better security

## Limitations

### Google Voice Limits

- **Fair Use:** ~100 messages/day
- **Polling:** 60-second delay
- **Unofficial API:** May break if Google changes
- **US Only:** Google Voice only available in US

### Not Recommended For

- High-volume production (>100 messages/day)
- Mission-critical alerts
- Real-time requirements (<60 second latency)
- International use

### Recommended For

- Personal use
- Testing and development
- Low-volume monitoring (<50 messages/day)
- Budget-conscious users
- Getting started

## Upgrading to Paid Service

### When to Upgrade

Consider upgrading to Twilio/Vonage if:
- Need more than 100 messages/day
- Need faster response (<60 seconds)
- Need guaranteed reliability
- Need official support
- Need international coverage

### Migration Path

1. Keep Google Voice for testing
2. Set up Twilio account
3. Configure Twilio in Settings
4. Test with both running
5. Switch to Twilio when ready
6. Keep Google Voice as backup

## Cost Comparison

### Google Voice
- **Setup:** FREE
- **Monthly:** FREE
- **Per Message:** FREE
- **Total:** $0/month

### Twilio (for comparison)
- **Setup:** FREE
- **Monthly:** $1 (phone number)
- **Per Message:** $0.0075
- **Total:** ~$1.75/month (100 messages)

### Savings
Using Google Voice saves ~$21/year!

## Advanced Tips

### Multiple Recipients

Send alerts to multiple numbers:
```
+1234567890, +0987654321, +1111111111
```

### Custom Check Interval

Adjust based on your needs:
- **Urgent:** 30 seconds
- **Normal:** 60 seconds
- **Relaxed:** 120 seconds

### Dedicated Number

Use Google Voice number exclusively for monitoring:
- Easier to manage
- Clear separation
- Professional appearance

### Message Templates

Train technicians to use consistent format:
```
Station 1 - 56.893
Station 2 - 104.295
```

## Support

### Google Voice Help
- [support.google.com/voice](https://support.google.com/voice)
- [Google Voice Community](https://support.google.com/voice/community)

### App Help
- Check Settings → Alert Notifications
- Verify receiver status (green = running)
- Check console for error messages
- Review this guide

### Common Issues
- **Login fails:** Use App Password
- **No messages:** Check phone number matches
- **Slow receiving:** Normal (60-second polling)
- **Rate limited:** Reduce message volume

## Summary

Google Voice provides a **completely FREE** solution for:
- ✅ Receiving SMS from technicians
- ✅ Sending SMS alerts
- ✅ Automatic message processing
- ✅ No monthly fees
- ✅ Easy setup

Perfect for personal use and getting started!

For production or high-volume use, consider upgrading to Twilio or Vonage.
