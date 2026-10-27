from fastapi.responses import JSONResponse


def api_response(status_code: int, success: bool, message: str, data=None, errors=None):
    content = {"success": success, "message": message}
    if data is not None:
        content["data"] = data
    if errors is not None:
        content["errors"] = errors
    return JSONResponse(status_code=status_code, content=content)
