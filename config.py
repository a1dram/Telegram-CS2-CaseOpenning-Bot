import json
import os
import random
import time

import logging
import asyncio

from time import perf_counter

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import *
from aiogram.filters import *
from aiogram.utils.markdown import hbold
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from utils.database import db
from utils.create_photo import download_skin_photo, load_skin_photo
from utils.settings import Settings

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

settings = Settings()