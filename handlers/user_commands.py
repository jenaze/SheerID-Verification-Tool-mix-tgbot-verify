"""用户命令处理器"""
import logging
from typing import Optional

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, CallbackQueryHandler

from config import ADMIN_USER_ID
from database_mysql import Database
from utils.checks import reject_group_command
from utils.messages import (
    get_welcome_message,
    get_about_message,
    get_help_message,
)
from utils.i18n import get_text, LANGUAGES

logger = logging.getLogger(__name__)


def get_main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """获取主菜单键盘"""
    keyboard = [
        [
            KeyboardButton(get_text("menu_verify", lang)),
            KeyboardButton(get_text("menu_balance", lang))
        ],
        [
            KeyboardButton(get_text("menu_checkin", lang)),
            KeyboardButton(get_text("menu_invite", lang))
        ],
        [
            KeyboardButton(get_text("menu_language", lang)),
            KeyboardButton(get_text("menu_help", lang))
        ]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /start 命令"""
    if await reject_group_command(update):
        return

    user = update.effective_user
    user_id = user.id
    username = user.username or ""
    full_name = user.full_name or ""

    # 获取语言，如果用户未注册则默认为en
    lang = "en"
    if db.user_exists(user_id):
        lang = db.get_user_language(user_id)
        msg = get_text("welcome_back", lang, full_name=full_name)
        await update.message.reply_text(
            msg,
            reply_markup=get_main_menu_keyboard(lang)
        )
        return

    # 邀请参与
    invited_by: Optional[int] = None
    if context.args:
        try:
            invited_by = int(context.args[0])
            if not db.user_exists(invited_by):
                invited_by = None
        except Exception:
            invited_by = None

    # 创建用户
    if db.create_user(user_id, username, full_name, invited_by):
        welcome_msg = get_welcome_message(full_name, bool(invited_by), lang)

        # 提示选择语言
        keyboard = [
            [
                InlineKeyboardButton("English", callback_data="lang_en"),
                InlineKeyboardButton("简体中文", callback_data="lang_zh")
            ],
            [
                InlineKeyboardButton("فارسی", callback_data="lang_fa"),
                InlineKeyboardButton("العربية", callback_data="lang_ar")
            ]
        ]

        await update.message.reply_text(
            welcome_msg,
            reply_markup=get_main_menu_keyboard(lang)
        )

        await update.message.reply_text(
            get_text("language_select", lang),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(get_text("registration_failed", lang))


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /language 命令"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", "en"))
        return

    lang = db.get_user_language(user_id)

    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="lang_en"),
            InlineKeyboardButton("简体中文", callback_data="lang_zh")
        ],
        [
            InlineKeyboardButton("فارسی", callback_data="lang_fa"),
            InlineKeyboardButton("العربية", callback_data="lang_ar")
        ]
    ]

    await update.message.reply_text(
        get_text("language_select", lang),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理语言选择回调"""
    query = update.callback_query
    await query.answer()

    data = query.data
    if not data.startswith("lang_"):
        return

    lang_code = data.split("_")[1]
    user_id = update.effective_user.id

    if lang_code in LANGUAGES:
        db.set_user_language(user_id, lang_code)

        # 更新界面语言
        success_msg = get_text("language_set", lang_code)
        await query.edit_message_text(success_msg)

        # 发送新菜单
        await query.message.reply_text(
            get_text("menu_verify", lang_code), # Just a dummy message to show keyboard
            reply_markup=get_main_menu_keyboard(lang_code)
        )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /about 命令"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    await update.message.reply_text(get_about_message(lang), reply_markup=get_main_menu_keyboard(lang))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /help 命令"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"
    is_admin = user_id == ADMIN_USER_ID

    await update.message.reply_text(get_help_message(is_admin, lang), reply_markup=get_main_menu_keyboard(lang))


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /balance 命令"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text(get_text("not_registered", lang))
        return

    await update.message.reply_text(
        get_text("current_balance", lang, balance=user['balance']),
        reply_markup=get_main_menu_keyboard(lang)
    )


async def checkin_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /qd 签到命令"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    if not db.can_checkin(user_id):
        await update.message.reply_text(get_text("checkin_already", lang), reply_markup=get_main_menu_keyboard(lang))
        return

    if db.checkin(user_id):
        user = db.get_user(user_id)
        await update.message.reply_text(
            get_text("checkin_success", lang, balance=user['balance']),
            reply_markup=get_main_menu_keyboard(lang)
        )
    else:
        await update.message.reply_text(get_text("checkin_already", lang), reply_markup=get_main_menu_keyboard(lang))


async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /invite 邀请命令"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    bot_username = context.bot.username
    invite_link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        get_text("invite_message", lang, invite_link=invite_link),
        reply_markup=get_main_menu_keyboard(lang)
    )


async def use_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /use 命令 - 使用卡密"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    if not context.args:
        await update.message.reply_text(get_text("use_key_usage", lang))
        return

    key_code = context.args[0].strip()
    result = db.use_card_key(key_code, user_id)

    if result is None:
        await update.message.reply_text(get_text("key_not_found", lang))
    elif result == -1:
        await update.message.reply_text(get_text("key_limit_reached", lang))
    elif result == -2:
        await update.message.reply_text(get_text("key_expired", lang))
    elif result == -3:
        await update.message.reply_text(get_text("key_already_used", lang))
    else:
        user = db.get_user(user_id)
        await update.message.reply_text(
            get_text("key_success", lang, amount=result, balance=user['balance']),
            reply_markup=get_main_menu_keyboard(lang)
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理文本消息（菜单点击）"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"
    text = update.message.text

    # 简单的文本匹配
    if text == get_text("menu_verify", lang):
        # List all verification services
        msg = get_text("help_verify_commands", lang, cost=1, help_url="") # We reuse help_verify_commands
        await update.message.reply_text(msg, disable_web_page_preview=True)

    elif text == get_text("menu_balance", lang):
        await balance_command(update, context, db)

    elif text == get_text("menu_checkin", lang):
        await checkin_command(update, context, db)

    elif text == get_text("menu_invite", lang):
        await invite_command(update, context, db)

    elif text == get_text("menu_language", lang):
        await language_command(update, context, db)

    elif text == get_text("menu_help", lang):
        await help_command(update, context, db)
