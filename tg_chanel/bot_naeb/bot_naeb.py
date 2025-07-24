import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

import os
TOKEN = os.getenv('TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Описание тарифов
TARIFFS = {
    "pay_month": {
        "title": "📦 Тариф: на месяц (-25%)",
        "price": 549.00,
        "currency": "🇷🇺RUB",
        "duration": "месяц",
        "access": "• Anechka Privat (канал)",
        "note": "Привет котик.\nВ этом канале мои голые пися, попа и сиси. Если ты ещё не выбрал тариф — снизу другие (они лучше). Если выбрал этот — бегом оплачивать :))",
        "payment_details": {
            "receiver": "Иванова А.А.",
            "card": "2202 2006 7834 1442"
        }
    },
    "pay_forever": {
        "title": "📦 Тариф: навсегда (-20%)",
        "price": 799.00,
        "currency": "🇷🇺RUB",
        "duration": "бессрочный",
        "access": "• Anechka Privat (канал)",
        "note": "Привет котик.\nВ этом канале мои голые пися, попа и сиси. Если ты ещё не выбрал тариф — снизу другие (они лучше). Если выбрал этот — бегом оплачивать :))",
        "payment_details": {
            "receiver": "Иванова А.А.",
            "card": "2202 2006 7834 1442"
        }
    },
    "pay_mega_vip": {
        "title": "📦 Тариф: Mega вип",
        "price": 1199.00,
        "currency": "🇷🇺RUB",
        "duration": "бессрочный",
        "access": "• Эстетика❤️ (канал)",
        "note": "Ребята это канал только для самых - самых ярых моих поклонников. Для ценителей эстетической красоты и для тех кто всячески хочет поддержать меня и мой проект💙",
        "payment_details": {
            "receiver": "Иванова А.А.",
            "card": "2202 2006 7834 1442"
        }
    },
    "pay_special_video": {
        "title": "📦 Тариф: Отдельный тариф где меня трахают🔥",
        "price": 1499.00,
        "currency": "🇷🇺RUB",
        "duration": "бессрочный",
        "access": "• Шалости Анечки с её друзьями (канал)\n• Шалости с подружкой (канал)",
        "note": "",
        "payment_details": {
            "receiver": "Иванова А.А.",
            "card": "2202 2006 7834 1442"
        }
    }
}

# Главное меню (без приветствия)
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    builder = InlineKeyboardBuilder()
    for tariff_id, tariff_data in TARIFFS.items():
        builder.button(
            text=tariff_data["title"].split(" - ")[0], 
            callback_data=tariff_id
        )
    builder.adjust(1)

    await message.answer(
        "Приветствую в Приватке Анечки😘!\n"
        " \n"
        "Оплата через бота даёт преимущество:\n"
        "• Мгновенное получение ссылки-приглашения после оплаты, даже когда я не в сети\n\n"
        "‼️СКИДКИ ДО 30%‼️\n\n"
        "❤️ Цена входа:\n"
        "• Месяц — 549₽\n"
        "• Навсегда — 799₽\n"
        "• MEGA вип — 1199₽\n"
        "• Отдельный тариф🔥 — 1499₽",
        reply_markup=builder.as_markup()
    )

# Меню тарифа
@dp.callback_query(F.data.in_(TARIFFS.keys()))
async def process_tariff_choice(callback: types.CallbackQuery):
    tariff_id = callback.data
    tariff = TARIFFS[tariff_id]
    
    text = (
        f"{tariff['title']}\n"
        f"💰 Стоимость: {tariff['price']} {tariff['currency']}\n"
        f"📅 Срок действия: <b>{tariff['duration']}</b>\n\n"
        f"Вы получите доступ к:\n"
        f"{tariff['access']}\n\n"
        f"{tariff['note']}"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Назад", callback_data="go_back")
    builder.button(text="💳 Оплатить", callback_data=f"confirm_{tariff_id}")
    builder.adjust(1)

    await callback.message.edit_text(
        text,
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()

# Вернуться назад (исправлено дублирование)
@dp.callback_query(F.data == "go_back")
async def go_back(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    for tariff_id, tariff_data in TARIFFS.items():
        builder.button(
            text=tariff_data["title"].split(" - ")[0], 
            callback_data=tariff_id
        )
    builder.adjust(1)

    await callback.message.edit_text(
        "Оплата через бота даёт преимущество:\n"
        "• Мгновенное получение ссылки-приглашения после оплаты, даже когда я не в сети\n\n"
        "‼️СКИДКИ ДО 30%‼️\n\n"
        "❤️ Цена входа:\n"
        "• Месяц — 549₽\n"
        "• Навсегда — 799₽\n"
        "• MEGA вип — 1199₽\n"
        "• Отдельный тариф🔥 — 1499₽",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

# Подтверждение оплаты
@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    tariff_id = callback.data.replace("confirm_", "")
    tariff = TARIFFS[tariff_id]
    
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Я оплатил", callback_data=f"paid_{tariff_id}")
    builder.adjust(1)

    await callback.message.edit_text(
        f"<b>💳 Оплата тарифа</b>\n\n"
        f"💰 Сумма: {tariff['price']} {tariff['currency']}\n"
        f"👤 Получатель: {tariff['payment_details']['receiver']}\n"
        f"🏦 Номер карты: <code>{tariff['payment_details']['card']}</code>\n\n"
        "После перевода нажми на кнопку ниже.",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()

# Обработка нажатия "Я оплатил"
@dp.callback_query(F.data.startswith("paid_"))
async def paid_handler(callback: types.CallbackQuery):
    tariff_id = callback.data.replace("paid_", "")
    tariff = TARIFFS[tariff_id]
    user = callback.from_user

    # Сообщение админу
    admin_message = (
        "📩 <b>НОВАЯ ОПЛАТА</b>\n"
        f"👤 Пользователь: {user.full_name} "
        f"(<a href='tg://user?id={user.id}'>@{user.username}</a>, "
        f"ID: <code>{user.id}</code>)\n"
        f"📦 Тариф: <b>{tariff['title']}</b>\n"
        f"💰 Сумма: <b>{tariff['price']} {tariff['currency']}</b>"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="HTML")

    # Ответ пользователю
    await callback.message.edit_text(
        "Спасибо за оплату! Я проверю перевод и выдам доступ как можно скорее 💋\n\n"
        "Чтобы вернуться в меню, нажми /start"
    )
    await callback.answer()

# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    asyncio.run(main())
