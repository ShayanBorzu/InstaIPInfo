import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from BoxApi import public_info

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, I'm Working!"}


# Endpoint to get Instagram profile info by username
@app.get("/instagram_username/{username}")
async def instagram_username(username: str):
    try:
        info = await public_info(username)
        return JSONResponse(content=info)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoint to get IP information
@app.get("/ip_information/{ip}")
async def ip_information(ip: str):
    url = f"https://ipapi.co/{ip}/json/"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return JSONResponse(content=response.json())
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
