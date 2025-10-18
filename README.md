# InstaIPInfo

Asynchronous FastAPI backend service for Instagram profile information (boxapi.ir) and IP geolocation data retrieval (ipapi.co).

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
  "network": "8.8.8.0/24",
  "version": "IPv4",
  "city": "Mountain View",
  "region": "California",
  "region_code": "CA",
  "country": "US",
  "country_name": "United States",
  "country_code": "US",
  "country_code_iso3": "USA",
  "country_capital": "Washington",
  "country_tld": ".us",
  "continent_code": "NA",
  "in_eu": false,
  "postal": "94043",
  "latitude": 37.42301,
  "longitude": -122.083352,
  "timezone": "America/Los_Angeles",
  "utc_offset": "-0700",
  "country_calling_code": "+1",
  "currency": "USD",
  "currency_name": "Dollar",
  "languages": "en-US,es-US,haw,fr",
  "country_area": 9629091,
  "country_population": 327167434,
  "asn": "AS15169",
  "org": "GOOGLE"
}
```

## Environment Variables / Secrets

Store your BoxAPI credentials securely and do not commit them to version control. Place your credentials in `vault.py` or set them as environment variables as used by the project.

## License

This project is licensed under the MIT License.