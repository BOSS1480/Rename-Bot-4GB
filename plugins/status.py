import psutil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN

def progress_bar(percent: float, length: int = 10) -> str:
    filled = int(percent / (100 / length))
    return "█" * filled + "░" * (length - filled)

@Client.on_message(filters.command("status") & filters.user(ADMIN))
async def status_cmd(client, message):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    text = (
        f"**🤖 Bot Status**\n\n"
        f"**CPU:** `{progress_bar(cpu)}` {cpu:.1f}%\n"
        f"**RAM:** `{progress_bar(mem.percent)}` {mem.percent:.1f}% — "
        f"{mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB\n"
        f"**Disk:** `{progress_bar(disk.percent)}` {disk.percent:.1f}% — "
        f"{disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB\n"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Refresh", callback_data="status_refresh")],
        [InlineKeyboardButton("✖️ Close", callback_data="cancel")]
    ])

    await message.reply(text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("^status_refresh$") & filters.user(ADMIN))
async def refresh_status(client, query):
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    text = (
        f"**🤖 Bot Status**\n\n"
        f"**CPU:** `{progress_bar(cpu)}` {cpu:.1f}%\n"
        f"**RAM:** `{progress_bar(mem.percent)}` {mem.percent:.1f}% — "
        f"{mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB\n"
        f"**Disk:** `{progress_bar(disk.percent)}` {disk.percent:.1f}% — "
        f"{disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB\n"
    )
    await query.message.edit(text, reply_markup=query.message.reply_markup)
    await query.answer()
