import os
from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from config.bot_config import WEBHOOK_PATH
from config.bot_config import WEBHOOK_URL
from config.bot_config import BOT_URL
import uvicorn


def init_api(bot, dp):
    app = FastAPI()

    @app.on_event("startup")
    async def on_startup():
        webhook_info = await bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URL:
            await bot.set_webhook(
                url=WEBHOOK_URL
            )

    @app.post(WEBHOOK_PATH)
    async def bot_webhook(update: dict):
        telegram_update = types.Update(**update)
        Dispatcher.set_current(dp)
        Bot.set_current(bot)
        await dp.process_update(telegram_update)

    @app.on_event("shutdown")
    async def on_shutdown():
        await bot.get_session()

    uvicorn.run(app, host=BOT_URL, port=int(os.getenv("PORT", 5010)))
