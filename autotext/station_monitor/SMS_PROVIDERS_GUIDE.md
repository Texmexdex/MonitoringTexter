# SMS Providers Guide

This guide covers all supported SMS providers for sending alert notifications.

## Supported Providers

1. **Google Voice** - FREE! Use your existing Google Voice account
2. **Twilio** - Most popular, reliable, easy to use
3. **Vonage (Nexmo)** - Good alternative, competitive pricing
4. **AWS SNS** - If you're already using AWS
5. **Custom Webhook** - Use your own SMS gateway

---

## 1. Google Voice (FREE!)

### Overview
- **Cost:** FREE! 🎉
- **Reliability:** Good
- **Setup Time:** 5 minutes
- **Best For:** Personal use, testing, budget-conscious

### Setup Steps

1. **Get Google Voice** (if you don't have it)
   - Go to [voice.google.com](https://voice.google.com)
   - Sign in with your Google account
   - Get a free phone number

2. **Enable Less Secure Apps or App Password**
   
   **Option A: App Password (Recommended)**
   - Go to [myaccount.google.com/security](https://myaccount.google.com/security)
   - Enable 2-Step Verification
   - Go to App Passwords
   - Generate password for "Mail"
   - Copy the 16-character password
   
   **Option B: Less Secure Apps** (Not recommended)
   - Go to [myaccount.google.com/lesssecureapps](https://myaccount.google.com/lesssecureapps)
   - Turn on "Allow less secure apps"

3. **Install googlevoice Library**
   ```bash
   pip install googlevoice
   ```

4. **Configure in App**
   - Settings → Alert Notifications
   - Enable SMS Notifications
   - Select Provider: **google_voice**
   - Enter your Gmail address
   - Enter your App Password (or regular password)
   - Enter To Numbers
   - Save Settings

### Pricing
- **Completely FREE!** 🎉
- No monthly fees
- No per-message costs
- Unlimited texts (within Google's fair use)

### Pros
- Absolutely free
- No credit card required
- Easy setup
- Works with existing Google account
- Good for personal use

### Cons
- Requires Google Voice account
- May have rate limits
- Less reliable than paid services
- Not recommended for high-volume production
- Requires googlevoice library

### Limitations
- Google may rate limit excessive usage
- Not officially supported API (uses unofficial library)
- May break if Google changes their system
- Best for personal/testing use

### Installation
```bash
pip install googlevoice
```

---

## 2. Twilio

## 1. Twilio

### Overview
- **Cost:** ~$0.0075 per SMS (US), $1/month for phone number
- **Reliability:** Excellent
- **Setup Time:** 10 minutes
- **Best For:** Most users, production use

### Setup Steps

1. **Sign up at [twilio.com](https://twilio.com)**
   - Create free account
   - Verify your email and phone

2. **Get a Phone Number**
   - Go to Phone Numbers → Buy a Number
   - Choose a number (~$1/month)
   - Enable SMS capability

3. **Get Credentials**
   - Go to Console Dashboard
   - Copy **Account SID** (starts with AC...)
   - Copy **Auth Token** (click to reveal)

4. **Configure in App**
   - Settings → Alert Notifications
   - Enable SMS Notifications
   - Select Provider: **twilio**
   - Enter Account SID
   - Enter Auth Token
   - Enter From Number (your Twilio number)
   - Enter To Numbers (comma-separated)
   - Save Settings

### Pricing
- **US/Canada:** $0.0075 per SMS
- **International:** Varies by country
- **Phone Number:** $1/month
- **Free Trial:** $15 credit

### Pros
- Very reliable
- Great documentation
- Easy to use
- Excellent delivery rates
- Good support

### Cons
- Requires credit card after trial
- Monthly phone number fee

---

## 2. Vonage (Nexmo)

### Overview
- **Cost:** ~$0.0057 per SMS (US)
- **Reliability:** Excellent
- **Setup Time:** 10 minutes
- **Best For:** Cost-conscious users, international

### Setup Steps

1. **Sign up at [vonage.com](https://www.vonage.com/communications-apis/)**
   - Create account
   - Verify email

2. **Get API Credentials**
   - Go to Dashboard
   - Copy **API Key**
   - Copy **API Secret**

3. **Get a Virtual Number** (Optional)
   - Go to Numbers → Buy Numbers
   - Or use alphanumeric sender ID (some countries)

4. **Configure in App**
   - Settings → Alert Notifications
   - Enable SMS Notifications
   - Select Provider: **vonage**
   - Enter API Key
   - Enter API Secret
   - Enter From Number (or brand name)
   - Enter To Numbers
   - Save Settings

### Pricing
- **US:** $0.0057 per SMS
- **International:** Competitive rates
- **Virtual Number:** ~$0.90/month
- **Free Trial:** €2 credit

### Pros
- Slightly cheaper than Twilio
- Good international coverage
- Alphanumeric sender ID support
- No monthly fees (if using sender ID)

### Cons
- Less popular than Twilio
- Documentation not as extensive

---

## 3. AWS SNS (Simple Notification Service)

### Overview
- **Cost:** $0.00645 per SMS (US)
- **Reliability:** Excellent
- **Setup Time:** 15 minutes
- **Best For:** AWS users, high volume

### Setup Steps

1. **AWS Account Required**
   - Sign up at [aws.amazon.com](https://aws.amazon.com)
   - Enable SNS service

2. **Create IAM User**
   - Go to IAM → Users → Add User
   - Enable Programmatic Access
   - Attach Policy: `AmazonSNSFullAccess`
   - Save Access Key ID and Secret Key

3. **Request SMS Spending Limit Increase**
   - By default, AWS limits SMS to $1/month
   - Go to SNS → Text Messaging (SMS)
   - Request limit increase

4. **Install boto3**
   ```bash
   pip install boto3
   ```

5. **Configure in App**
   - Settings → Alert Notifications
   - Enable SMS Notifications
   - Select Provider: **aws_sns**
   - Enter Access Key ID
   - Enter Secret Access Key
   - Enter Region (e.g., us-east-1)
   - Enter To Numbers
   - Save Settings

### Pricing
- **US:** $0.00645 per SMS
- **International:** Varies
- **No monthly fees**
- **Pay only for what you use**

### Pros
- Cheapest option
- No monthly fees
- Scales automatically
- Integrated with AWS ecosystem

### Cons
- Requires AWS account
- More complex setup
- Default spending limit ($1/month)
- Requires boto3 library

### Note
AWS SNS integration requires the `boto3` library. Install it:
```bash
pip install boto3
```

---

## 4. Custom Webhook

### Overview
- **Cost:** Depends on your gateway
- **Reliability:** Depends on your gateway
- **Setup Time:** Varies
- **Best For:** Custom integrations, existing SMS gateway

### Use Cases
- You have an existing SMS gateway
- Using a different SMS provider
- Corporate SMS system
- Android SMS gateway app
- Custom integration

### Setup Steps

1. **Set Up Your Webhook Endpoint**
   - Must accept POST requests
   - Must return 200 OK on success

2. **Expected Request Format**
   ```json
   POST https://your-gateway.com/send
   Headers:
     Content-Type: application/json
     Authorization: Bearer YOUR_API_KEY (if configured)
   
   Body:
   {
     "to_numbers": ["+1234567890", "+0987654321"],
     "message": "Alert: Station 1 out of range...",
     "type": "alert"
   }
   ```

3. **Configure in App**
   - Settings → Alert Notifications
   - Enable SMS Notifications
   - Select Provider: **webhook**
   - Enter Webhook URL
   - Enter API Key (optional)
   - Enter To Numbers
   - Save Settings

### Example Webhook Implementation

#### Node.js/Express
```javascript
app.post('/send', async (req, res) => {
  const { to_numbers, message } = req.body;
  
  // Send SMS via your gateway
  for (const number of to_numbers) {
    await yourSmsGateway.send(number, message);
  }
  
  res.status(200).json({ success: true });
});
```

#### Python/Flask
```python
@app.route('/send', methods=['POST'])
def send_sms():
    data = request.json
    to_numbers = data['to_numbers']
    message = data['message']
    
    # Send SMS via your gateway
    for number in to_numbers:
        your_sms_gateway.send(number, message)
    
    return jsonify({'success': True}), 200
```

### Android SMS Gateway
Use apps like:
- SMS Gateway API
- SMS Gateway for Android
- Tasker + AutoRemote

---

## Comparison Table

| Provider | Cost (US) | Setup | Reliability | Best For |
|----------|-----------|-------|-------------|----------|
| **Google Voice** | FREE! | Easy | ⭐⭐⭐⭐ | Personal/Testing |
| **Twilio** | $0.0075/SMS + $1/mo | Easy | ⭐⭐⭐⭐⭐ | Production |
| **Vonage** | $0.0057/SMS | Easy | ⭐⭐⭐⭐⭐ | Cost-conscious |
| **AWS SNS** | $0.00645/SMS | Medium | ⭐⭐⭐⭐⭐ | AWS users |
| **Webhook** | Varies | Varies | Varies | Custom needs |

---

## Testing

### Test Your Configuration

1. Go to Settings → Alert Notifications
2. Enable SMS Notifications
3. Configure your provider
4. Enter your phone number in "To Numbers"
5. Save Settings
6. Go to Manual Entry
7. Submit a reading out of range
8. You should receive an SMS alert

### Test Message Format

The SMS will look like:
```
⚠️ Alert: Station 1 Out of Range

Alert: Station 1

Status: ABOVE maximum (125.50 > 120.0)
Current Value: 125.50
Safe Range: 50.0 - 120.0
Station Phone: +1234567890

Action Required: Contact technician to adjust readings.
```

---

## Troubleshooting

### SMS Not Received

**Check Configuration:**
- Provider credentials correct?
- Phone numbers in E.164 format (+1234567890)?
- SMS notifications enabled?
- Provider selected correctly?

**Check Provider:**
- Twilio: Check logs in console
- Vonage: Check delivery receipts
- AWS SNS: Check CloudWatch logs
- Webhook: Check your server logs

**Common Issues:**
- Invalid phone number format
- Insufficient credits/balance
- Provider account not verified
- Spending limits reached
- Network/connectivity issues

### Invalid Phone Number

Phone numbers must be in E.164 format:
- ✅ Correct: `+1234567890`
- ❌ Wrong: `(123) 456-7890`
- ❌ Wrong: `1234567890`

### Provider Errors

**Twilio:**
- Error 21211: Invalid phone number
- Error 21608: Unverified number (trial)
- Error 20003: Authentication failed

**Vonage:**
- Status 1: Throttled
- Status 2: Missing params
- Status 3: Invalid credentials

**AWS SNS:**
- InvalidParameter: Bad phone number
- Throttling: Rate limit exceeded
- AccessDenied: IAM permissions

---

## Cost Estimation

### Example: 100 Alerts/Month

| Provider | Monthly Cost |
|----------|--------------|
| **Google Voice** | **$0.00 (FREE!)** |
| Twilio | $1.75 ($0.75 SMS + $1 number) |
| Vonage | $0.57 (no number fee) |
| AWS SNS | $0.65 (no fees) |
| Webhook | Varies |

### Example: 1000 Alerts/Month

| Provider | Monthly Cost |
|----------|--------------|
| **Google Voice** | **$0.00 (FREE!)** |
| Twilio | $8.50 |
| Vonage | $5.70 |
| AWS SNS | $6.45 |

---

## Security Best Practices

### Credentials
- Never share API keys
- Store securely (config.json is local only)
- Rotate regularly
- Use environment variables in production

### Phone Numbers
- Validate before saving
- Use E.164 format
- Don't expose in logs
- Respect privacy regulations

### Rate Limiting
- Monitor usage
- Set spending limits
- Alert on unusual activity
- Implement retry logic

---

## Recommendations

### For Personal Use / Testing
→ **Google Voice**
- Completely free
- Easy setup
- Perfect for getting started
- Good for low-volume alerts

### For Production / Business
→ **Twilio**
- Most reliable
- Professional support
- Good documentation
- Worth the cost for critical alerts

### For Cost Savings (Production)
→ **Vonage** or **AWS SNS**
- Slightly cheaper than Twilio
- Still very reliable
- Good for high volume

### For Custom Needs
→ **Webhook**
- Maximum flexibility
- Use existing infrastructure
- Custom integrations

---

## Support

### Provider Support
- **Twilio:** [support.twilio.com](https://support.twilio.com)
- **Vonage:** [developer.vonage.com/support](https://developer.vonage.com/support)
- **AWS:** [aws.amazon.com/support](https://aws.amazon.com/support)

### Documentation
- **Twilio:** [twilio.com/docs/sms](https://www.twilio.com/docs/sms)
- **Vonage:** [developer.vonage.com/messaging/sms](https://developer.vonage.com/messaging/sms)
- **AWS SNS:** [docs.aws.amazon.com/sns](https://docs.aws.amazon.com/sns)

### App Settings
- Check Settings → Alert Notifications
- Verify provider configuration
- Test with manual entry
- Check config.json for saved settings
