from workers import Response

async def on_fetch(request):
    if request.method == "OPTIONS":
        # Handle CORS preflight
        return Response("", status=204, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        })

    if request.method != "POST":
        return Response("Use POST with a 'code' field", status=405)

    try:
        raw = await request.json()
        data = raw.to_py()
        code = data.get("code", "")

        sandbox = {}
        exec(code, sandbox)
        result = sandbox.get("output", "No 'output' variable defined.")

        return Response(str(result), headers={
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "text/plain"
        })

    except Exception as e:
        return Response(f"Execution error: {e}", status=400, headers={
            "Access-Control-Allow-Origin": "*"
        })