import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey123')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'real_estate_db')
    MYSQL_CURSORCLASS = 'DictCursor'
    # ============================================================
# Real Estate Listing Platform - Configuration File
# Developer  : Romil Pawar
# Copyright  : © 2026 Romil Pawar. All Rights Reserved.
# ============================================================