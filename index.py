from workers import Response
import base64

# Main handler for incoming HTTP requests
async def on_fetch(request):
    # Handle CORS preflight requests
    if request.method == "OPTIONS":
        return Response("", status=204, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        })

    # Only allow POST requests for code execution
    if request.method != "POST":
        return Response("Use POST with a 'code' field", status=405)

    try:
        # Parse JSON body from the request
        raw = await request.json()
        data = raw.to_py()
        # If 'file' is present, assume it's a base64-encoded .txt file with Python code
        if "file" in data:
            file_b64 = data["file"]
            code_bytes = base64.b64decode(file_b64)
            code = code_bytes.decode("utf-8")
        else:
            code = data.get("code", "")

        # Execute the provided code in a sandboxed dictionary
        sandbox = {}
        exec(code, sandbox)
        # Retrieve the 'output' variable from the sandbox, if defined
        result = sandbox.get("output", "No 'output' variable defined.")

        # Return the result with CORS and content-type headers
        return Response(str(result), headers={
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "text/plain"
        })

    except Exception as e:
        # Handle and return any execution errors
        return Response(f"Execution error: {e}", status=400, headers={
            "Access-Control-Allow-Origin": "*"
        })