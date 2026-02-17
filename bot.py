"""Telegram 机器人主程序"""
import logging
from functools import partial

import httpx
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram.request import HTTPXRequest

from config import BOT_TOKEN
from database_mysql import Database
from handlers.user_commands import (
    start_command,
    about_command,
    help_command,
    balance_command,
    checkin_command,
    invite_command,
    use_command,
    language_command,
    language_callback,
    handle_message,
)
from handlers.verify_commands import (
    verify_command,
    verify2_command,
    verify3_command,
    verify4_command,
    verify6_command,
    getV4Code_command,
)
from handlers.admin_commands import (
    addbalance_command,
    block_command,
    white_command,
    blacklist_command,
    genkey_command,
    listkeys_command,
    broadcast_command,
)

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context) -> None:
    """全局错误处理"""
    logger.exception("处理更新时发生异常: %s", context.error, exc_info=context.error)


def main():
    """主函数"""
    # 初始化数据库
    db = Database()

    # 配置更稳定的 HTTP 请求设置
    # 增加超时时间和连接池大小，减少网络波动导致的错误
    request = HTTPXRequest(
        connection_pool_size=100,  # 增大连接池
        read_timeout=30.0,         # 读取超时 30 秒
        write_timeout=30.0,        # 写入超时 30 秒
        connect_timeout=30.0,      # 连接超时 30 秒
        pool_timeout=10.0,         # 连接池超时 10 秒
    )

    # 创建应用 - 启用并发处理，使用自定义请求配置
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .request(request)          # 🔥 使用自定义请求配置
        .concurrent_updates(True)  # 🔥 启用并发处理多个命令
        .build()
    )

    # 注册用户命令（使用 partial 传递 db 参数）
    application.add_handler(CommandHandler("start", partial(start_command, db=db)))
    application.add_handler(CommandHandler("about", partial(about_command, db=db)))
    application.add_handler(CommandHandler("help", partial(help_command, db=db)))
    application.add_handler(CommandHandler("balance", partial(balance_command, db=db)))
    application.add_handler(CommandHandler("qd", partial(checkin_command, db=db)))
    application.add_handler(CommandHandler("invite", partial(invite_command, db=db)))
    application.add_handler(CommandHandler("use", partial(use_command, db=db)))
    application.add_handler(CommandHandler("language", partial(language_command, db=db)))

    # 注册消息处理器（菜单点击）
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, partial(handle_message, db=db)))

    # 注册回调查询处理器（语言选择）
    application.add_handler(CallbackQueryHandler(partial(language_callback, db=db)))

    # 注册验证命令
    application.add_handler(CommandHandler("verify", partial(verify_command, db=db)))
    application.add_handler(CommandHandler("verify2", partial(verify2_command, db=db)))
    application.add_handler(CommandHandler("verify3", partial(verify3_command, db=db)))
    application.add_handler(CommandHandler("verify4", partial(verify4_command, db=db)))
    application.add_handler(CommandHandler("verify6", partial(verify6_command, db=db)))
    application.add_handler(CommandHandler("getV4Code", partial(getV4Code_command, db=db)))

    # 注册管理员命令
    application.add_handler(CommandHandler("addbalance", partial(addbalance_command, db=db)))
    application.add_handler(CommandHandler("block", partial(block_command, db=db)))
    application.add_handler(CommandHandler("white", partial(white_command, db=db)))
    application.add_handler(CommandHandler("blacklist", partial(blacklist_command, db=db)))
    application.add_handler(CommandHandler("genkey", partial(genkey_command, db=db)))
    application.add_handler(CommandHandler("listkeys", partial(listkeys_command, db=db)))
    application.add_handler(CommandHandler("broadcast", partial(broadcast_command, db=db)))

    # 注册错误处理器
    application.add_error_handler(error_handler)

    logger.info("机器人启动中...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
