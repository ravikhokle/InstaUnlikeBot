import os

from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

if not USERNAME or not PASSWORD:
	raise ValueError("Missing IG_USERNAME or IG_PASSWORD in .env")
