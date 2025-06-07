"""
Simple HTTP server to capture and display incoming request headers and content.
For development and debugging.
"""

import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestCaptureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.capture_and_respond()

    def do_POST(self):
        self.capture_and_respond()

    def do_PUT(self):
        self.capture_and_respond()

    def do_DELETE(self):
        self.capture_and_respond()

    def do_PATCH(self):
        self.capture_and_respond()

    def capture_and_respond(self):
        # Print separator
        print("\n" + "=" * 60)
        print(f"📨 NEW REQUEST - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Print request line
        print(f"🔗 {self.command} {self.path} {self.request_version}")

        # Print headers
        print("\n📋 HEADERS:")
        for header in sorted(self.headers.keys()):
            print(f"   {header}: {self.headers[header]}")

        # Read and print body content
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            print(f"\n📄 BODY ({content_length} bytes):")
            try:
                # Try to parse as JSON for pretty printing
                json_data = json.loads(body.decode("utf-8"))
                print(json.dumps(json_data, indent=2))
            except:
                # If not JSON, print as string
                try:
                    print(body.decode("utf-8"))
                except:
                    print(f"Binary data: {body}")
        else:
            print("\n📄 BODY: (empty)")

        # Send a simple response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # For CORS
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

        response = {
            "status": "received",
            "method": self.command,
            "path": self.path,
            "timestamp": datetime.now().isoformat(),
        }
        self.wfile.write(json.dumps(response, indent=2).encode())

    def do_OPTIONS(self):
        # Handle preflight requests for CORS
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        )
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging to keep output clean
        pass


def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestCaptureHandler)

    print(f"🚀 HTTP Request Capture Server starting on port {port}")
    print(f"📡 Listening at: http://localhost:{port}")
    print("🔍 All incoming requests will be displayed below")
    print("⏹️  Press Ctrl+C to stop the server\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        httpd.shutdown()


if __name__ == "__main__":
    import sys

    # Allow custom port via command line argument
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")

    run_server(port)
