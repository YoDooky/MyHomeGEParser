from typing import List, Dict
from aiogram import types
from aiogram.utils.markdown import hbold, hlink


async def send_ad_to_chat(call: types.CallbackQuery, useful_data: List):
    for item in useful_data:
        media = get_ad_form(item)
        await call.message.answer_media_group(media=media)


def get_ad_form(item: Dict):
    """Send ad to chat"""
    card = f'{hlink(item.get("title"), item.get("url"))}\n' \
           f'{hbold("💵 цена: ")} {item.get("price")} $\n' \
           f'{hbold("🇬🇪 адрес: ")} {item.get("address")}\n' \
           f'{hbold("🛏 комнат: ")} {item.get("room")}\n' \
           f'{hbold("🏠 площадь: ")} {item.get("size")}m²\n' \
           f'{hbold("⏳ дата объявления: ")} {item.get("date")}'
    media = types.MediaGroup()
    img_list = parse_images(item.get('img_url'))
    for num, each in enumerate(img_list):
        if num > 9:
            break
        if not num:  # add caption to all media (works only if add caption on first img)
            media.attach_photo(types.InputMediaPhoto(each, caption=card))
            continue
        media.attach_photo(types.InputMediaPhoto(each))
    return media


def parse_images(img_string: str) -> List:
    return img_string.split(', ')
