# SMS Integration Guide

The Settings screen allows you to configure how the application receives text messages.

## Available Methods

### 1. Manual Entry (Current)
**Status:** ✅ Working Now  
**Cost:** Free  
**Setup:** None needed

Simply enter readings manually as you receive text messages.

---

### 2. Google Voice (NEW!)
**Status:** ✅ Working Now  
**Cost:** FREE!  
**Setup Time:** 5 minutes

#### How It Works:
1. Technicians text your Google Voice number
2. App polls Google Voice for new messages
3. Automatically parses and stores readings
4. Sends alerts if out of range

#### Setup Steps:
1. Get a Google Voice number at [voice.google.com](https://voice.google.com)
2. Create App Password (Settings → Security → App Passwords)
3. Install googlevoice: `pip install googlevoice`
4. In app Settings:
   - Select SMS Method: **Google Voice**
   - Enter Gmail address
   - Enter App Password
   - Set check interval (default: 60 seconds)
   - Click "Start Receiver"
5. Give your Google Voice number to technicians

#### Pros:
- Completely FREE!
- Automatic message receiving
- No monthly fees
- Easy setup
- Works great for personal use

#### Cons:
- Polling-based (checks every 60 seconds)
- Unofficial API (may break)
- Not for high-volume production
- Requires googlevoice library

---

### 3. Twilio SMS
**Status:** 🔜 Coming Soon  
**Cost:** ~$1-2/month  
**Setup Time:** 15 minutes

#### How It Works:
1. Technicians text a Twilio phone number
2. Twilio forwards messages to your app automatically
3. App parses and stores readings

#### Setup Steps:
1. Sign up at [twilio.com](https://twilio.com)
2. Purchase a phone number (~$1/month)
3. Get your Account SID and Auth Token
4. Enter credentials in Settings → Twilio Configuration
5. Configure webhook URL in Twilio console

#### Pros:
- Most reliable
- Professional solution
- Works from anywhere
- No phone needed

#### Cons:
- Monthly cost
- Requires internet

---

### 3. Email Forwarding
**Status:** 🔜 Coming Soon  
**Cost:** Free  
**Setup Time:** 10 minutes

#### How It Works:
1. Forward texts to an email address
2. App checks email inbox periodically
3. Parses messages from email

#### Setup Steps:
1. Set up text-to-email forwarding on your phone
2. Create a dedicated email account (recommended)
3. Enable IMAP access
4. Enter credentials in Settings → Email Configuration
5. Set check interval (default: 60 seconds)

#### Gmail Setup:
- IMAP Server: `imap.gmail.com`
- Port: `993`
- Use an App Password (not your regular password)
- Enable "Less secure app access" or use 2FA + App Password

#### Pros:
- Completely free
- No third-party service
- Works with existing email

#### Cons:
- Slight delay (polling interval)
- Less reliable than Twilio
- Email credentials stored locally

---

### 4. Webhook Receiver
**Status:** 🔜 Coming Soon  
**Cost:** Free  
**Setup Time:** 30 minutes (advanced)

#### How It Works:
1. App runs a local web server
2. External services POST messages to webhook URL
3. App receives and processes immediately

#### Setup Steps:
1. Configure port in Settings → Webhook Configuration
2. Ensure port is accessible (firewall/router)
3. Configure external service to POST to webhook URL
4. Format: `POST http://your-ip:port/webhook`
5. JSON body: `{"phone": "+1234567890", "message": "Station 1 - 56.893"}`

#### Use Cases:
- Custom SMS gateway
- Integration with other systems
- Android SMS gateway apps
- Zapier/IFTTT automation

#### Pros:
- Free
- Flexible
- Real-time
- Custom integrations

#### Cons:
- Requires technical knowledge
- Network configuration needed
- Security considerations

---

## Recommended Approach

### For Testing:
Start with **Manual Entry** to verify station ranges and workflow.

### For Production:
- **Small scale (< 10 messages/day):** Manual Entry or Email Forwarding
- **Medium scale (10-50 messages/day):** Twilio SMS
- **Large scale (50+ messages/day):** Twilio SMS
- **Custom integration:** Webhook Receiver

---

## Security Notes

### Credentials Storage:
- All credentials stored locally in `config.json`
- File is not encrypted (keep secure)
- Do not share config.json file

### Best Practices:
1. Use dedicated email account for email forwarding
2. Use app-specific passwords (not main password)
3. Keep Twilio auth token secret
4. Use HTTPS for webhook if exposed to internet
5. Regularly rotate credentials

---

## Troubleshooting

### Twilio Not Receiving:
- Verify Account SID and Auth Token
- Check Twilio phone number is correct
- Ensure webhook URL is configured in Twilio console
- Check Twilio logs for errors

### Email Not Working:
- Verify IMAP server and port
- Check email/password are correct
- Enable IMAP access in email settings
- Use app password for Gmail
- Check firewall isn't blocking

### Webhook Not Receiving:
- Verify port is open
- Check firewall settings
- Ensure correct URL format
- Test with curl or Postman
- Check app logs for errors

---

## Future Features

Coming in future updates:
- ✅ Twilio SMS integration
- ✅ Email forwarding integration
- ✅ Webhook receiver
- 🔜 SMS notifications (send alerts via SMS)
- 🔜 Email notifications
- 🔜 Multiple notification channels
- 🔜 Custom parsing rules per station
- 🔜 Auto-response messages

---

## Support

For help with SMS integration:
1. Check this guide
2. Review Settings screen tooltips
3. Test connection buttons
4. Check application logs

For Twilio support: [twilio.com/docs](https://www.twilio.com/docs)  
For Gmail IMAP: [support.google.com](https://support.google.com/mail/answer/7126229)
