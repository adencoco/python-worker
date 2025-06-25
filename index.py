from workers import Response

async def on_fetch(request):
    if request.method != "POST":
        return Response("Use POST with a 'code' field", status=405)

    try:
        raw = await request.json()
        data = raw.to_py()  # ← this is the correct way to convert JsProxy to dict

        code = data.get("code", "")

        sandbox = {}
        exec(code, sandbox)
        result = sandbox.get("output", "No 'output' variable defined.")
        return Response(str(result), headers={"content-type": "text/plain"})

    except Exception as e:
        return Response(f"Execution error: {e}", status=400)