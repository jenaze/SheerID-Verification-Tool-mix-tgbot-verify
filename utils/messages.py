"""消息模板 (Localized)"""
from config import CHANNEL_URL, VERIFY_COST, HELP_NOTION_URL
from utils.i18n import get_text


def get_welcome_message(full_name: str, invited_by: bool = False, lang: str = "en") -> str:
    """获取欢迎消息"""
    msg = get_text("welcome_title", lang, full_name=full_name) + "\n"

    if invited_by:
        msg += get_text("welcome_invited", lang) + "\n"
    else:
        msg += get_text("welcome_registered", lang) + "\n"

    msg += get_text("welcome_intro", lang, channel_url=CHANNEL_URL)
    return msg


def get_about_message(lang: str = "en") -> str:
    """获取关于消息"""
    return get_text("about_message", lang, channel_url=CHANNEL_URL)


def get_help_message(is_admin: bool = False, lang: str = "en") -> str:
    """获取帮助消息"""
    msg = get_text("help_title", lang) + "\n\n"
    msg += get_text("help_user_commands", lang)
    msg += get_text("help_verify_commands", lang, cost=VERIFY_COST, help_url=HELP_NOTION_URL) + "\n"

    if is_admin:
        # Admin commands are not localized yet, keep them in Chinese or English
        msg += (
            "\n管理员命令 (Admin):\n"
            "/addbalance <用户ID> <积分> - 增加用户积分\n"
            "/block <用户ID> - 拉黑用户\n"
            "/white <用户ID> - 取消拉黑\n"
            "/blacklist - 查看黑名单\n"
            "/genkey <卡密> <积分> [次数] [天数] - 生成卡密\n"
            "/listkeys - 查看卡密列表\n"
            "/broadcast <文本> - 向所有用户群发通知\n"
        )

    return msg


def get_insufficient_balance_message(current_balance: int, lang: str = "en") -> str:
    """获取积分不足消息"""
    return get_text("insufficient_balance", lang, cost=VERIFY_COST, balance=current_balance)


def get_verify_usage_message(command: str, service_name: str, lang: str = "en") -> str:
    """获取验证命令使用说明"""
    return get_text("verify_usage", lang, command=command, service_name=service_name)
