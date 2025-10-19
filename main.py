from fastapi import FastAPI
from fastapi.responses import JSONResponse
from APIHandeling import public_info, get_ip_info

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, I'm Working!"}


# Endpoint to get Instagram profile info by username
@app.get("/instagram_username/{username}")
async def instagram_username(username: str):
    info = await public_info(username)
    return JSONResponse(content=info)


# Endpoint to get IP information
@app.get("/ip_information/{ip}")
async def ip_information(ip: str):
    info = await get_ip_info(ip)
    return JSONResponse(content=info)
