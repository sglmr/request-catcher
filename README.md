# HTTP Request Capture Server

A simple Python HTTP server for capturing and displaying incoming request headers and content. Perfect for development, debugging, and testing webhooks.

## Features

- 🔍 Captures all HTTP methods (GET, POST, PUT, DELETE, PATCH, OPTIONS)
- 📋 Displays headers in a clean, readable format
- 📄 Shows request body content with JSON pretty-printing
- 🌐 Handles CORS for browser-based requests
- ⏰ Timestamps each request
- 🔗 Returns a simple JSON acknowledgment response
- 🚀 Easy to use with ngrok for external access

## Quick Start

1. Save the script as `capture_server.py`
2. Run the server:
   ```bash
   python capture_server.py
   ```
3. Server starts on `http://localhost:8000`

### Custom Port

```bash
# Run on port 3000
python capture_server.py 3000
```

## Example Output

When a request is received, you'll see output like this:

```
============================================================
📨 NEW REQUEST - 2025-06-07 14:30:25
============================================================
🔗 POST /api/webhook HTTP/1.1

📋 HEADERS:
   Host: localhost:8000
   Content-Type: application/json
   Content-Length: 45
   User-Agent: curl/7.68.0

📄 BODY (45 bytes):
{
  "event": "user.created",
  "user_id": 12345
}
```

## Testing with curl

### Simple GET Request
```bash
curl http://localhost:8000/test
```

### POST with JSON Data
```bash
curl -X POST http://localhost:8000/api/webhook \
     -H "Content-Type: application/json" \
     -d '{"event": "user.created", "user_id": 12345}'
```

### POST with Form Data
```bash
curl -X POST http://localhost:8000/form \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "name=John&email=john@example.com"
```

### Custom Headers
```bash
curl -X POST http://localhost:8000/api/data \
     -H "Authorization: Bearer your-token-here" \
     -H "X-Custom-Header: custom-value" \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello World"}'
```

## Using with ngrok for External Access

To allow external services to reach your local server:

### 1. Install ngrok
```bash
# macOS (Homebrew)
brew install ngrok/ngrok/ngrok

# Windows (Chocolatey)
choco install ngrok

# Linux (snap)
sudo snap install ngrok
```

### 2. Set up ngrok (one-time)
```bash
# Get your auth token from https://ngrok.com
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

### 3. Run both services

**Terminal 1** - Start the capture server:
```bash
python capture_server.py 8000
```

**Terminal 2** - Start ngrok tunnel:
```bash
ngrok http 8000
```

### 4. Use the public URL

ngrok will show output like:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8000
```

Now external services can send requests to `https://abc123.ngrok-free.app`

### Test the public URL
```bash
curl -X POST https://abc123.ngrok-free.app/webhook \
     -H "Content-Type: application/json" \
     -d '{"test": "from external service"}'
```

## Common Use Cases

### Webhook Development
Perfect for testing webhook integrations from services like:
- GitHub webhooks
- Stripe payment notifications
- Slack app events
- Discord bot interactions
- Twilio SMS callbacks

### API Testing
- Test your API client implementations
- Debug request formatting issues
- Verify headers and authentication tokens
- Inspect request payloads

### CORS Testing
The server includes CORS headers, making it useful for testing browser-based requests:
```javascript
// Works from browser console
fetch('http://localhost:8000/test', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({message: 'from browser'})
});
```

## Response Format

The server responds with a JSON acknowledgment:
```json
{
  "status": "received",
  "method": "POST",
  "path": "/api/webhook",
  "timestamp": "2025-06-07T14:30:25.123456"
}
```

## Stopping the Server

Press `Ctrl+C` to stop the server gracefully.

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Security Note

This server is designed for development and testing only. It should not be used in production environments as it:
- Logs all request data (including sensitive information)
- Has no authentication or rate limiting
- Accepts all origins for CORS

## Troubleshooting

### Port Already in Use
```bash
# Try a different port
python capture_server.py 8001
```

### ngrok Warning Page
Free ngrok URLs show a warning page for first-time visitors. Users can click "Visit Site" to continue, or upgrade to a paid plan to remove the warning.

### Firewall Issues
Ensure your firewall allows incoming connections on the chosen port for local testing.