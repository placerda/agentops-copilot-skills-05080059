from http.server import BaseHTTPRequestHandler, HTTPServer
import json


RESPONSES = {
    "Where is my order ORD-12345?": "Order ORD-12345 is in transit and expected to arrive tomorrow.",
    "Can I return a damaged headset from ORD-77821?": "Yes. Start a return for ORD-77821 and choose damaged item as the reason.",
    "How do I contact a human support agent?": "I can connect you to a human support agent for account or order issues.",
}


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("content-length", "0"))
        body = json.loads(self.rfile.read(length))
        message = body.get("message", "")
        text = RESPONSES.get(message, "I can help with order status, returns, and support escalation.")

        payload = json.dumps({"text": text}).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


HTTPServer(("127.0.0.1", 8790), Handler).serve_forever()
