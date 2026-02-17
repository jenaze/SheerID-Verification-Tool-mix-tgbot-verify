"""验证命令处理器"""
import asyncio
import logging
import httpx
import time
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from config import VERIFY_COST
from database_mysql import Database
from one.sheerid_verifier import SheerIDVerifier as OneVerifier
from k12.sheerid_verifier import SheerIDVerifier as K12Verifier
from spotify.sheerid_verifier import SheerIDVerifier as SpotifyVerifier
from youtube.sheerid_verifier import SheerIDVerifier as YouTubeVerifier
from Boltnew.sheerid_verifier import SheerIDVerifier as BoltnewVerifier
from onestudent.sheerid_verifier import GeminiStudentVerifier
from utils.messages import get_insufficient_balance_message, get_verify_usage_message
from utils.i18n import get_text

# 尝试导入并发控制，如果失败则使用空实现
try:
    from utils.concurrency import get_verification_semaphore
except ImportError:
    # 如果导入失败，创建一个简单的实现
    def get_verification_semaphore(verification_type: str):
        return asyncio.Semaphore(3)

logger = logging.getLogger(__name__)


async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify 命令 - Gemini One Pro"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify", "Gemini One Pro", lang)
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"], lang)
        )
        return

    verification_id = OneVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text(get_text("invalid_link", lang))
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text(get_text("deduct_failed", lang))
        return

    processing_msg = await update.message.reply_text(
        get_text("verify_start", lang, service_name="Gemini One Pro", verification_id=verification_id, cost=VERIFY_COST)
    )

    try:
        verifier = OneVerifier(verification_id)
        result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "gemini_one_pro",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = get_text("verify_success", lang)
            if result.get("pending"):
                result_msg += get_text("verify_pending", lang)
            if result.get("redirect_url"):
                result_msg += get_text("verify_redirect", lang, url=result['redirect_url'])
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                get_text("verify_failed", lang, message=result.get('message', 'Unknown'), cost=VERIFY_COST)
            )
    except Exception as e:
        logger.error("验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            get_text("verify_error", lang, error=str(e), cost=VERIFY_COST)
        )


async def verify2_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify2 命令 - ChatGPT Teacher K12"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify2", "ChatGPT Teacher K12", lang)
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"], lang)
        )
        return

    verification_id = K12Verifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text(get_text("invalid_link", lang))
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text(get_text("deduct_failed", lang))
        return

    processing_msg = await update.message.reply_text(
        get_text("verify_start", lang, service_name="ChatGPT Teacher K12", verification_id=verification_id, cost=VERIFY_COST)
    )

    try:
        verifier = K12Verifier(verification_id)
        result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "chatgpt_teacher_k12",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = get_text("verify_success", lang)
            if result.get("pending"):
                result_msg += get_text("verify_pending", lang)
            if result.get("redirect_url"):
                result_msg += get_text("verify_redirect", lang, url=result['redirect_url'])
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                get_text("verify_failed", lang, message=result.get('message', 'Unknown'), cost=VERIFY_COST)
            )
    except Exception as e:
        logger.error("验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            get_text("verify_error", lang, error=str(e), cost=VERIFY_COST)
        )


async def verify3_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify3 命令 - Spotify Student"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify3", "Spotify Student", lang)
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"], lang)
        )
        return

    # 解析 verificationId
    verification_id = SpotifyVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text(get_text("invalid_link", lang))
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text(get_text("deduct_failed", lang))
        return

    processing_msg = await update.message.reply_text(
        get_text("verify_start_detailed", lang, service_name="Spotify Student", cost=VERIFY_COST)
    )

    # 使用信号量控制并发
    semaphore = get_verification_semaphore("spotify_student")

    try:
        async with semaphore:
            verifier = SpotifyVerifier(verification_id)
            result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "spotify_student",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = get_text("verify_success", lang)
            if result.get("pending"):
                result_msg += get_text("verify_pending", lang)
            if result.get("redirect_url"):
                result_msg += get_text("verify_redirect", lang, url=result['redirect_url'])
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                get_text("verify_failed", lang, message=result.get('message', 'Unknown'), cost=VERIFY_COST)
            )
    except Exception as e:
        logger.error("Spotify 验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            get_text("verify_error", lang, error=str(e), cost=VERIFY_COST)
        )


async def verify4_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify4 命令 - Bolt.new Teacher（自动获取code版）"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify4", "Bolt.new Teacher", lang)
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"], lang)
        )
        return

    # 解析 externalUserId 或 verificationId
    external_user_id = BoltnewVerifier.parse_external_user_id(url)
    verification_id = BoltnewVerifier.parse_verification_id(url)

    if not external_user_id and not verification_id:
        await update.message.reply_text(get_text("invalid_link", lang))
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text(get_text("deduct_failed", lang))
        return

    processing_msg = await update.message.reply_text(
        get_text("bolt_start", lang, cost=VERIFY_COST)
    )

    # 使用信号量控制并发
    semaphore = get_verification_semaphore("bolt_teacher")

    try:
        async with semaphore:
            # 第1步：提交文档
            verifier = BoltnewVerifier(url, verification_id=verification_id)
            result = await asyncio.to_thread(verifier.verify)

        if not result.get("success"):
            # 提交失败，退款
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                get_text("bolt_doc_failed", lang, message=result.get('message', 'Unknown'), cost=VERIFY_COST)
            )
            return
        
        vid = result.get("verification_id", "")
        if not vid:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                get_text("verify_failed", lang, message="No verification ID returned", cost=VERIFY_COST)
            )
            return
        
        # 更新消息
        await processing_msg.edit_text(
            get_text("bolt_submitted", lang, vid=vid)
        )
        
        # 第2步：自动获取认证码（最多20秒）
        code = await _auto_get_reward_code(vid, max_wait=20, interval=5)
        
        if code:
            # 成功获取
            result_msg = get_text("bolt_success_code", lang, code=code)
            if result.get("redirect_url"):
                result_msg += get_text("verify_redirect", lang, url=result['redirect_url'])
            
            await processing_msg.edit_text(result_msg)
            
            # 保存成功记录
            db.add_verification(
                user_id,
                "bolt_teacher",
                url,
                "success",
                f"Code: {code}",
                vid
            )
        else:
            # 20秒内未获取到，让用户稍后查询
            await processing_msg.edit_text(
                get_text("bolt_pending_code", lang, vid=vid)
            )
            
            # 保存待处理记录
            db.add_verification(
                user_id,
                "bolt_teacher",
                url,
                "pending",
                "Waiting for review",
                vid
            )
            
    except Exception as e:
        logger.error("Bolt.new 验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            get_text("verify_error", lang, error=str(e), cost=VERIFY_COST)
        )


async def _auto_get_reward_code(
    verification_id: str,
    max_wait: int = 20,
    interval: int = 5
) -> Optional[str]:
    """自动获取认证码（轻量级轮询，不影响并发）"""
    import time
    start_time = time.time()
    attempts = 0
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            elapsed = int(time.time() - start_time)
            attempts += 1
            
            # 检查是否超时
            if elapsed >= max_wait:
                logger.info(f"自动获取code超时({elapsed}秒)，让用户手动查询")
                return None
            
            try:
                # 查询验证状态
                response = await client.get(
                    f"https://my.sheerid.com/rest/v2/verification/{verification_id}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    current_step = data.get("currentStep")
                    
                    if current_step == "success":
                        # 获取认证码
                        code = data.get("rewardCode") or data.get("rewardData", {}).get("rewardCode")
                        if code:
                            logger.info(f"✅ 自动获取code成功: {code} (耗时{elapsed}秒)")
                            return code
                    elif current_step == "error":
                        # 审核失败
                        logger.warning(f"审核失败: {data.get('errorIds', [])}")
                        return None
                    # else: pending，继续等待
                
                # 等待下次轮询
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.warning(f"查询认证码出错: {e}")
                await asyncio.sleep(interval)
    
    return None


async def verify5_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify5 命令 - YouTube Student Premium"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify5", "YouTube Student Premium", lang)
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"], lang)
        )
        return

    # 解析 verificationId
    verification_id = YouTubeVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text(get_text("invalid_link", lang))
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text(get_text("deduct_failed", lang))
        return

    processing_msg = await update.message.reply_text(
        get_text("verify_start_detailed", lang, service_name="YouTube Student Premium", cost=VERIFY_COST)
    )

    # 使用信号量控制并发
    semaphore = get_verification_semaphore("youtube_student")

    try:
        async with semaphore:
            verifier = YouTubeVerifier(verification_id)
            result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "youtube_student",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = get_text("verify_success", lang)
            if result.get("pending"):
                result_msg += get_text("verify_pending", lang)
            if result.get("redirect_url"):
                result_msg += get_text("verify_redirect", lang, url=result['redirect_url'])
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                get_text("verify_failed", lang, message=result.get('message', 'Unknown'), cost=VERIFY_COST)
            )
    except Exception as e:
        logger.error("YouTube 验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            get_text("verify_error", lang, error=str(e), cost=VERIFY_COST)
        )


async def verify6_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /verify6 命令 - Gemini One Student (45+ Universities)"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify6", "Gemini One Student (Advanced)", lang)
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"], lang)
        )
        return

    # 解析 verificationId
    verification_id = GeminiStudentVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text(get_text("invalid_link", lang))
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text(get_text("deduct_failed", lang))
        return

    processing_msg = await update.message.reply_text(
        get_text("verify_start_detailed", lang, service_name="Gemini One Student", cost=VERIFY_COST)
    )

    # 使用信号量控制并发
    semaphore = get_verification_semaphore("gemini_student")

    try:
        async with semaphore:
            verifier = GeminiStudentVerifier(verification_id)
            result = await verifier.verify()

        db.add_verification(
            user_id,
            "gemini_student",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = get_text("verify_success", lang)
            result_msg += f"👤 Student: {result.get('student', 'N/A')}\n"
            result_msg += f"🆔 Student ID: {result.get('student_id', 'N/A')}\n"
            result_msg += f"📧 Email: {result.get('email', 'N/A')}\n"
            result_msg += f"🏫 School: {result.get('school', 'N/A')}\n"
            
            if result.get("pending"):
                result_msg += get_text("verify_pending", lang)
            
            if result.get("redirect_url"):
                result_msg += get_text("verify_redirect", lang, url=result['redirect_url'])
            
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                get_text("verify_failed", lang, message=result.get('message', 'Unknown'), cost=VERIFY_COST)
            )
    except Exception as e:
        logger.error("Gemini Student 验证过程出错: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            get_text("verify_error", lang, error=str(e), cost=VERIFY_COST)
        )


async def getV4Code_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """处理 /getV4Code 命令 - 获取 Bolt.new Teacher 认证码"""
    user_id = update.effective_user.id
    lang = db.get_user_language(user_id) if db.user_exists(user_id) else "en"

    if db.is_user_blocked(user_id):
        await update.message.reply_text(get_text("blocked_user", lang))
        return

    if not db.user_exists(user_id):
        await update.message.reply_text(get_text("not_registered", lang))
        return

    # 检查是否提供了 verification_id
    if not context.args:
        await update.message.reply_text(get_text("bolt_code_usage", lang))
        return

    verification_id = context.args[0].strip()

    processing_msg = await update.message.reply_text(get_text("bolt_query_wait", lang))

    try:
        # 查询 SheerID API 获取认证码
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"https://my.sheerid.com/rest/v2/verification/{verification_id}"
            )

            if response.status_code != 200:
                await processing_msg.edit_text(
                    get_text("bolt_query_failed", lang, status=response.status_code)
                )
                return

            data = response.json()
            current_step = data.get("currentStep")
            reward_code = data.get("rewardCode") or data.get("rewardData", {}).get("rewardCode")
            redirect_url = data.get("redirectUrl")

            if current_step == "success" and reward_code:
                result_msg = get_text("bolt_success_code", lang, code=reward_code)
                if redirect_url:
                    result_msg += get_text("verify_redirect", lang, url=redirect_url)
                await processing_msg.edit_text(result_msg)
            elif current_step == "pending":
                await processing_msg.edit_text(get_text("bolt_query_pending", lang))
            elif current_step == "error":
                error_ids = data.get("errorIds", [])
                await processing_msg.edit_text(
                    get_text("verify_failed", lang, message=', '.join(error_ids) if error_ids else 'Unknown', cost=0)
                )
            else:
                await processing_msg.edit_text(
                    get_text("bolt_query_no_code", lang, status=current_step)
                )

    except Exception as e:
        logger.error("获取 Bolt.new 认证码失败: %s", e)
        await processing_msg.edit_text(
            get_text("bolt_query_failed", lang, status=str(e))
        )
