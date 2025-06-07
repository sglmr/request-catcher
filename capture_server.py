#!/usr/bin/env python3
"""
Simple HTTP server to capture and display incoming request headers and content.
Perfect for development and debugging.
"""

import json
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestCaptureHandler(BaseHTTPRequestHandler):
    # Class variable to track request counter
    request_counter = 0

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

    def save_request_to_file(self, timestamp, content_length, body):
        """Save request details to a timestamped file"""
        # Increment counter for unique filenames
        RequestCaptureHandler.request_counter += 1

        # Create requests directory if it doesn't exist
        if not os.path.exists("requests"):
            os.makedirs("requests")

        # Create filename with timestamp and counter
        filename = f"requests/request_{timestamp.strftime('%Y%m%d_%H%M%S')}_{RequestCaptureHandler.request_counter:03d}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(
                    f"HTTP Request Capture - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                f.write("=" * 60 + "\n\n")

                # Request line
                f.write("REQUEST LINE:\n")
                f.write(f"{self.command} {self.path} {self.request_version}\n\n")

                # Headers
                f.write("HEADERS:\n")
                for header in sorted(self.headers.keys()):
                    f.write(f"{header}: {self.headers[header]}\n")

                # Body
                f.write(f"\nBODY ({content_length} bytes):\n")
                if content_length > 0:
                    try:
                        # Try to parse as JSON for pretty printing
                        json_data = json.loads(body.decode("utf-8"))
                        f.write(json.dumps(json_data, indent=2))
                    except:
                        # If not JSON, write as string
                        try:
                            f.write(body.decode("utf-8"))
                        except:
                            f.write(f"Binary data (length: {len(body)} bytes)")
                else:
                    f.write("(empty)")

                f.write("\n")

            return filename
        except Exception as e:
            print(f"❌ Error saving request to file: {e}")
            return None

    def capture_and_respond(self):
        timestamp = datetime.now()

        # Print separator
        print("\n" + "=" * 60)
        print(f"📨 NEW REQUEST - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Print request line
        print(f"🔗 {self.command} {self.path} {self.request_version}")

        # Print headers (sorted alphabetically)
        print("\n📋 HEADERS:")
        for header in sorted(self.headers.keys()):
            print(f"   {header}: {self.headers[header]}")

        # Read and print body content
        content_length = int(self.headers.get("Content-Length", 0))
        body = b""
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

        # Save to file if enabled
        if hasattr(self.server, "save_requests") and self.server.save_requests:
            filename = self.save_request_to_file(timestamp, content_length, body)
            if filename:
                print(f"💾 Request saved to: {filename}")

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
            "timestamp": timestamp.isoformat(),
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


def run_server(port=8000, save_requests=False):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestCaptureHandler)
    httpd.save_requests = save_requests  # Add save_requests attribute to server

    print(f"🚀 HTTP Request Capture Server starting on port {port}")
    print(f"📡 Listening at: http://localhost:{port}")
    print("🔍 All incoming requests will be displayed below")
    if save_requests:
        print("💾 Requests will be saved to ./requests/ directory")
    print("⏹️  Press Ctrl+C to stop the server\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        httpd.shutdown()


if __name__ == "__main__":
    import sys

    # Parse command line arguments
    port = 8000
    save_requests = False

    for arg in sys.argv[1:]:
        if arg == "--save" or arg == "-s":
            save_requests = True
        elif arg.startswith("--port="):
            try:
                port = int(arg.split("=")[1])
            except ValueError:
                print("Invalid port number. Using default port 8000.")
        elif arg.isdigit():
            # Backwards compatibility - port as first argument
            port = int(arg)
        elif arg in ["--help", "-h"]:
            print("HTTP Request Capture Server")
            print("Usage: python capture_server.py [port] [--save]")
            print("  port         Port number (default: 8000)")
            print("  --save, -s   Save requests to files")
            print("  --port=N     Specify port number")
            print("  --help, -h   Show this help")
            sys.exit(0)

    run_server(port, save_requests)
