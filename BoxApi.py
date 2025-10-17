import httpx
import base64
from httpx import BasicAuth
from vault import boxapi_username, boxapi_password

async def image_url_to_base64(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30)
        response.raise_for_status()
        return base64.b64encode(response.content).decode("utf-8")

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
    except httpx.HTTPError as e:
        raise Exception(f"Error fetching data for username {username}: {e}")
