#!/usr/bin/env python3
"""encrypt_password module"""

import bcrypt

def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a password is valid"""
    return bcrypt.checkpw(password.encode(), hashed_password)
