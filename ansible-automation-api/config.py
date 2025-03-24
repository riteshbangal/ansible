import os

AWX_URL = "http://localhost:8080/api/v2"
AWX_ADMIN_USER = "admin"
AWX_ADMIN_PASSWORD = os.getenv("AWX_ADMIN_PASSWORD")

if not AWX_ADMIN_PASSWORD:
    raise ValueError("AWX_ADMIN_PASSWORD environment variable is not set.")
