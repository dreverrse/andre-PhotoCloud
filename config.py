import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    UPLOAD_FOLDER = "uploads"
    THUMB_FOLDER = "thumbnails"

    MAX_LOGIN_ATTEMPT = 5
    BLOCK_TIME = 300