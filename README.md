# HTTP Request Capture Server

A simple Python HTTP server for capturing and displaying incoming requests. Perfect for webhook development and API testing.

## Features

- Captures all HTTP methods with headers and body content
- Optional file saving for detailed inspection  
- CORS support for browser testing
- Works with ngrok for external access

## Quick Start

```bash
# Basic usage
python capture_server.py

# With file saving
python capture_server.py --save

# Custom port and file saving
python capture_server.py 8080 --save
```

## Command Options

```bash
python capture_server.py [port] [--save] [--help]
```

- `port` - Port number (default: 8000)
- `--save` - Save requests to `./requests/` directory
- `--help` - Show help

## Testing Examples

```bash
# Simple POST
curl -X POST http://localhost:8000/webhook \
     -H "Content-Type: application/json" \
     -d '{"event": "test"}'

# With custom headers
curl -X POST http://localhost:8000/api \
     -H "Authorization: Bearer token123" \
     -H "Content-Type: application/json" \
     -d '{"data": "value"}'
```

## External Access with ngrok

1. **Install ngrok**: Download from https://ngrok.com
2. **Set up auth**: `ngrok config add-authtoken YOUR_TOKEN`
3. **Run server**: `python capture_server.py 8000 --save`
4. **Start tunnel**: `ngrok http 8000`
5. **Use public URL**: External services can now reach `https://abc123.ngrok-free.app`

## Output Example

```
📨 NEW REQUEST - 2025-06-07 14:30:25
🔗 POST /webhook HTTP/1.1

📋 HEADERS:
   Content-Type: application/json
   User-Agent: curl/7.68.0

📄 BODY (25 bytes):
{"event": "test"}

💾 Request saved to: requests/request_20250607_143025_001.txt
```

## Use Cases

- **Webhook testing** - GitHub, Stripe, Slack integrations
- **API debugging** - Inspect headers, auth tokens, payloads
- **CORS testing** - Browser-based request validation

## Requirements

Python 3.6+ (no external dependencies)