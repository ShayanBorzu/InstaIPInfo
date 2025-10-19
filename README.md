# InstaIPInfo

Asynchronous FastAPI backend service for Instagram profile information (boxapi.ir) and IP geolocation data retrieval (ipapi.co, abstractapi.com, ipgeolocation.io 80,000 req/month).

## Installation

```bash
git clone https://github.com/ShayanBorzu/InstaIPInfo
```
```bash
cd your-project
```
```bash
python -m venv venv
```
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
```bash
pip install -r requirements.txt
```

Create a file named `vault.py` with these variables:

```python
boxapi_username = 'your_boxapi_username'
boxapi_password = 'your_boxapi_password'

ABSTRACTAPI_TOKEN = 'your_abstractapi_token' # abstractapi.com

IPGEOLOCATION_TOKEN = 'your_ipgeolocation_token' # ipgeolocation.io
```

## Usage

Run the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

### Get Instagram user info

**Request:**

```
GET http://127.0.0.1:8000/instagram_username/google
```

**Response example:**

```json
{
  "full_name": "Google",
  "profile_picture": "/9j/4AAQSkZJRgABAQAAAQABAAD/7QCEUGhvd...",
  "biography": "Here to help.",
  "following_count": 39,
  "followers_count": 15667847,
  "posts_count": 2959
}
```

### Get IP geolocation info

**Request:**

```
GET http://127.0.0.1:8000/ip_information/8.8.8.8
```

**Response example:**

```json
{
  "ip": "8.8.8.8",
  "org": "GOOGLE",
  "country_name": "United States",
  "region": "California",
  "city": "Mountain View",
  "latitude": 37.42301,
  "longitude": -122.083352,
  "timezone": "America/Los_Angeles",
  "information_source": "ipapi.co"
}
```

## Environment Variables / Secrets

Store your BoxAPI credentials securely and do not commit them to version control. Place your credentials in `vault.py` or set them as environment variables as used by the project.

## License

This project is licensed under the MIT License.