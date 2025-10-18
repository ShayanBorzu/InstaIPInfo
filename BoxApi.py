import httpx
import base64
from httpx import BasicAuth, RequestError, HTTPStatusError
from vault import boxapi_username, boxapi_password
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
                    print(f"Attempt {attempt} failed: {e}. Retrying in {wait_time} seconds...")
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

        full_name = user.get("full_name")
        profile_pic_url = user.get("profile_pic_url_hd")
        profile_picture = await image_url_to_base64(profile_pic_url) if profile_pic_url else None
        biography = user.get("biography")
        following_count = user.get("edge_follow", {}).get("count", 0)
        followers_count = user.get("edge_followed_by", {}).get("count", 0)
        posts_count = user.get("edge_owner_to_timeline_media", {}).get("count", 0)

        return {
            "full_name": full_name,
            "profile_picture": profile_picture,
            "biography": biography,
            "following_count": following_count,
            "followers_count": followers_count,
            "posts_count": posts_count,
        }

    except httpx.HTTPStatusError as e:
        print(f"HTTP status error {e.response.status_code}: {e.response.text}")
        raise Exception(f"Error fetching data for username {username}: {e.response.status_code}")

    except httpx.RequestError as e:
        print(f"Network error: {str(e)}")
        raise Exception(f"Network error fetching data for username {username}: {str(e)}")
