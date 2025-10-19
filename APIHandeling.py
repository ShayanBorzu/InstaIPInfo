import httpx
import base64
from httpx import BasicAuth
from vault import (
    boxapi_username,
    boxapi_password,
    ABSTRACTAPI_TOKEN,
    IPGEOLOCATION_TOKEN,
)
from fastapi import HTTPException
import asyncio
import functools


# This decorator will retry the function up to 'retries' times with an exponential backoff
def fetch_with_retries(retries=3, backoff_factor=0.5):
    def decorator_fetch(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries:
                        raise
                    wait_time = backoff_factor * (2 ** (attempt - 1))
                    print(
                        f"Attempt {attempt} failed: {e}. Retrying in {wait_time} seconds..."
                    )
                    await asyncio.sleep(wait_time)

        return wrapper

    return decorator_fetch


# Internal helper function to convert image URL to base64
async def image_url_to_base64(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30)
        response.raise_for_status()
        return base64.b64encode(response.content).decode("utf-8")


# Main function to get public Instagram profile info
@fetch_with_retries(retries=5, backoff_factor=1)
async def public_info(username: str) -> dict:
    url = "https://boxapi.ir/api/instagram/user/get_web_profile_info"
    auth = BasicAuth(boxapi_username, boxapi_password)
    json_data = {"username": username}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, auth=auth, json=json_data)
            response.raise_for_status()
            data = response.json()

        user = data.get("response", {}).get("body", {}).get("data", {}).get("user", {})

        full_name = user.get("full_name") or None

        profile_pic_url = user.get("profile_pic_url_hd")
        profile_picture = (
            await image_url_to_base64(profile_pic_url) if profile_pic_url else None
        )

        biography = user.get("biography")

        following_count = user.get("edge_follow", {}).get("count", 0)
        followers_count = user.get("edge_followed_by", {}).get("count", 0)

        posts_count = user.get("edge_owner_to_timeline_media", {}).get("count", 0)

        polished_data = {
            "full_name": full_name,
            "profile_picture": profile_picture,
            "biography": biography,
            "following_count": following_count,
            "followers_count": followers_count,
            "posts_count": posts_count,
        }

        return polished_data
    except httpx.HTTPStatusError as e:
        print(f"HTTP status error {e.response.status_code}: {e.response.text}")
        raise Exception(
            f"Error fetching data for username {username}: {e.response.status_code}"
        )

    except httpx.RequestError as e:
        print(f"Network error: {str(e)}")
        raise Exception(
            f"Network error fetching data for username {username}: {str(e)}"
        )


# Internal helper function to get IP information (ipapi.co) free: 30,000 requests per month limit
@fetch_with_retries(retries=5, backoff_factor=0.2)
async def ipapi_co(ip: str) -> dict:
    url = f"https://ipapi.co/{ip}/json/"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        polished_data = {
            "ip": ip,
            "org": data.get("org", "N/A"),
            "country_name": data.get("country_name", "N/A"),
            "region": data.get("region", "N/A"),
            "city": data.get("city", "N/A"),
            "latitude": data.get("latitude", "N/A"),
            "longitude": data.get("longitude", "N/A"),
            "timezone": data.get("timezone", "N/A"),
            "information_source": "ipapi.co",
        }
        return polished_data
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


# Internal helper function to get IP information (abstractapi.com) free: 20,000 requests per month limit (sign in required)
@fetch_with_retries(retries=5, backoff_factor=0.2) 
async def abstractapi_com(ip: str) -> dict:
    url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={ABSTRACTAPI_TOKEN}&ip_address={ip}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            connection = data.get("connection") or {}
            timezone = data.get("timezone") or {}

            polished_data = {
                "ip": ip,
                "org": connection.get("autonomous_system_organization", "N/A"),
                "country_name": data.get("country", "N/A"),
                "region": data.get("region", "N/A"),
                "city": data.get("city", "N/A"),
                "latitude": data.get("latitude", "N/A"),
                "longitude": data.get("longitude", "N/A"),
                "timezone": timezone.get("name", "N/A"),
                "information_source": "abstractapi.com",
            }
        return polished_data
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


# Internal helper function to get IP information (ipgeolocation.io) free: 1000 requests per day limit (sign in required)
@fetch_with_retries(retries=5, backoff_factor=0.2)
async def ipgeolocation_io(ip: str) -> dict:
    url = (
        f"https://api.ipgeolocation.io/v2/timezone?apiKey={IPGEOLOCATION_TOKEN}&ip={ip}"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            org = data.get("organization") or {}
            location = data.get("location") or {}
            timezone = data.get("timezone") or {}

            polished_data = {
                "ip": ip,
                "org": org.get("name", "N/A"),
                "country_name": location.get("country_name", "N/A"),
                "region": location.get("state_prov", "N/A"),
                "city": location.get("city", "N/A"),
                "latitude": location.get("latitude", "N/A"),
                "longitude": location.get("longitude", "N/A"),
                "timezone": timezone.get("name", "N/A"),
                "information_source": "ipgeolocation.io",
            }
            return polished_data
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


# Main function to get IP address Information
async def get_ip_info(ip: str) -> dict:
    get_ip_info_services = [ipapi_co, abstractapi_com, ipgeolocation_io]
    for service in get_ip_info_services:
        try:
            data = await service(ip)
            if data is not None:
                return data
        except Exception:
            continue
    return {"error": "All services failed to retrieve IP information."}
