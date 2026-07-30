"""
    File: /launcher.py
    Usage: Sets up logging, runs the bot, and hosts a web server for Hugging Face.
"""
import asyncio
from logging import getLogger
import os
import sys

from discord import Intents
from discord.ext.commands import when_mentioned_or
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

from redonhub import Bot, config, __version__ as version
from redonhub.utils.logging import setup_logging

load_dotenv(os.getcwd() + "/.env")

_log = getLogger(__name__)
handler = None

# ==========================================
# 1. إنشاء سيرفر الويب لـ Hugging Face
# ==========================================
web_app = FastAPI()

@web_app.get("/")
async def health_check():
    return {"status": "Bot is alive and running 24/7!"}

async def start_web_server():
    server_config = uvicorn.Config(web_app, host="0.0.0.0", port=7860, log_level="warning")
    server = uvicorn.Server(server_config)
    await server.serve()

# ==========================================
# 2. إعداد البوت الأصلي بتاعك
# ==========================================
bot = Bot(
    when_mentioned_or(config.Bot.Prefix),
    intents=Intents.all(),
    # Everything below is only required for the cogs to run, not the bot itself.
    version=version,
    owner_ids=config.Bot.Owners,
)


async def run():
    with setup_logging():
        token = os.getenv("token")
        if token is None:
            _log.critical("No token found in .env file.")
            sys.exit(1)

        if os.getenv("database") is None:
            _log.critical("No database found in .env file.")
            sys.exit(1)

        # ==========================================
        # 3. تشغيل سيرفر الويب في الخلفية مع البوت
        # ==========================================
        asyncio.create_task(start_web_server())

        try:
            await bot.start(token)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            _log.error("An error occurred while running the bot.")
            _log.exception(e)
        finally:
            sys.exit(0)


if __name__ == "__main__":
    asyncio.run(run())
