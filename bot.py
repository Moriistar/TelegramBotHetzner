import json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from hetzner_api import HetznerAPI

# Load config
with open("config.json") as f:
    config = json.load(f)

ADMIN_ID = config["admin_id"]
BOT_TOKEN = config["bot_token"]
HETZNER_TOKEN = config["hetzner_token"]

api = HetznerAPI(HETZNER_TOKEN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ شما اجازه استفاده از این ربات را ندارید.")

    keyboard = [
        [InlineKeyboardButton("🟢 ساخت سرور", callback_data="create")],
        [InlineKeyboardButton("📋 لیست سرورها", callback_data="list")],
        [InlineKeyboardButton("🗑 حذف سرور", callback_data="delete")],
        [InlineKeyboardButton("🔄 ریبوت سرور", callback_data="reboot")],
        [InlineKeyboardButton("♻ رینستال", callback_data="rebuild")],
    ]
    await update.message.reply_text("مدیریت هرتزنر:", reply_markup=InlineKeyboardMarkup(keyboard))


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user.id

    if user != ADMIN_ID:
        return await query.answer("اجازه دسترسی ندارید", show_alert=True)

    await query.answer()

    if query.data == "create":
        await query.edit_message_text("نام سرور را ارسال کنید:")
        context.user_data["action"] = "create"

    elif query.data == "list":
        servers = api.list_servers()
        text = "📋 *لیست سرورها:*\n\n"
        for s in servers["servers"]:
            text += f"ID: `{s['id']}` - {s['name']} - {s['status']}\n"
        await query.edit_message_text(text, parse_mode="Markdown")

    elif query.data == "delete":
        await query.edit_message_text("🗑 لطفاً ID سرور را ارسال کن:")
        context.user_data["action"] = "delete"

    elif query.data == "reboot":
        await query.edit_message_text("🔄 ID سرور برای ریبوت:")
        context.user_data["action"] = "reboot"

    elif query.data == "rebuild":
        await query.edit_message_text("♻ ID سرور برای رینستال:")
        context.user_data["action"] = "rebuild"


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = context.user_data.get("action")

    if update.message.from_user.id != ADMIN_ID:
        return

    if action == "create":
        name = update.message.text
        result = api.create_server(name)
        await update.message.reply_text(f"سرور ساخته شد:\n```{result}```", parse_mode="Markdown")

    elif action == "delete":
        sid = update.message.text
        result = api.delete_server(sid)
        await update.message.reply_text(f"حذف شد:\n```{result}```", parse_mode="Markdown")

    elif action == "reboot":
        sid = update.message.text
        result = api.reboot_server(sid)
        await update.message.reply_text(f"ریستارت شد:\n```{result}```", parse_mode="Markdown")

    elif action == "rebuild":
        sid = update.message.text
        result = api.rebuild_server(sid)
        await update.message.reply_text(f"رینستال شد:\n```{result}```", parse_mode="Markdown")

    context.user_data["action"] = None


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("panel", start))
    app.add_handler(CommandHandler("admin", start))
    app.add_handler(CommandHandler("root", start))
    app.add_handler(CommandHandler("manage", start))
    app.add_handler(CommandHandler("servers", buttons))
    app.add_handler(CommandHandler("vps", buttons))
    app.add_handler(CommandHandler("list", buttons))
    app.add_handler(CommandHandler("delete", buttons))
    app.add_handler(CommandHandler("restart", buttons))
    app.add_handler(CommandHandler("reinstall", buttons))
    app.add_handler(CommandHandler("rebuild", buttons))
    app.add_handler(CommandHandler("create", buttons))
    app.add_handler(CommandHandler("helpme", start))
    app.add_handler(CommandHandler("commands", start))
    app.add_handler(CommandHandler("info", start))
    app.add_handler(CommandHandler("about", start))
    app.add_handler(CommandHandler("settings", start))
    app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
