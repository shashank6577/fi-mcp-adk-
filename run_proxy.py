#!/usr/bin/env python3
import sys
import json
import threading
import httpx
from httpx_sse import httpx_sse

# 1) Start the mock server in the background (optional).
#    If you've already run `go run .` in fi-mcp-dev, you can skip this.
#    Otherwise uncomment below:
#
# import subprocess, os
# os.environ["FI_MCP_PORT"] = "8080"
# subprocess.Popen(["go", "run", "C:\\Users\\shubh\\OneDrive\\Desktop\\AI\\fi-mcp-dev"], shell=True)

client = httpx.Client()

def read_requests():
    """Read JSON-RPC requests from stdin and return them as dicts."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue

def write_response(resp_obj):
    """Write a JSON-RPC response object to stdout."""
    sys.stdout.write(json.dumps(resp_obj) + "\n")
    sys.stdout.flush()

def handle_request(req):
    """
    Translate a JSON-RPC request into an HTTP call to the mock server,
    then return a JSON-RPC response.
    """
    rid = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    # Map the RPC method name directly to the HTTP path:
    url = f"http://localhost:8080/mcp/{method}"
    try:
        r = client.get(url, params=params, timeout=10)
        r.raise_for_status()
        result = r.json()
        write_response({"jsonrpc": "2.0", "id": rid, "result": result})
    except Exception as e:
        write_response({
            "jsonrpc": "2.0",
            "id": rid,
            "error": {"code": -32000, "message": str(e)}
        })

def main():
    # Kick off a thread to read stdin in the background:
    for rpc in read_requests():
        handle_request(rpc)

if __name__ == "__main__":
    main()
