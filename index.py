#!/usr/bin/env python3
"""
Vercel serverless handler for Shaya Sussman Content Generator API.

This file serves as the entry point for Vercel's Python runtime.
It imports and exports the FastAPI app from api.py.
"""

from api import app

# Vercel requires a handler named 'handler' or an ASGI app named 'app'
# FastAPI is ASGI-compatible, so we just export 'app'
handler = app
