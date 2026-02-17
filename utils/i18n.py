"""Internationalization (i18n) support"""
from typing import Dict, Any

LANGUAGES = {
    "en": "English",
    "zh": "简体中文",
    "fa": "فارسی",
    "ar": "العربية",
}

DEFAULT_LANGUAGE = "en"

TRANSLATIONS = {
    # General
    "welcome_title": {
        "en": "🎉 Welcome, {full_name}!",
        "zh": "🎉 欢迎，{full_name}！",
        "fa": "🎉 خوش آمدید، {full_name}!",
        "ar": "🎉 أهلاً بك، {full_name}!",
    },
    "welcome_registered": {
        "en": "You have successfully registered and received 1 point.",
        "zh": "您已成功注册，获得 1 积分。",
        "fa": "شما با موفقیت ثبت نام کردید و ۱ امتیاز دریافت کردید.",
        "ar": "لقد قمت بالتسجيل بنجاح وحصلت على نقطة واحدة.",
    },
    "welcome_invited": {
        "en": "Thanks for joining via an invite link! The inviter has received 2 points.",
        "zh": "感谢通过邀请链接加入，邀请人已获得 2 积分。",
        "fa": "از اینکه از طریق لینک دعوت پیوستید متشکریم! دعوت کننده ۲ امتیاز دریافت کرده است.",
        "ar": "شكراً لانضمامك عبر رابط الدعوة! لقد حصل الداعي على نقطتين.",
    },
    "welcome_intro": {
        "en": "\nThis bot can automatically complete SheerID verifications.\n\nQuick Start:\n/about - About the bot\n/balance - Check balance\n/help - Full command list\n\nGet more points:\n/qd - Daily check-in\n/invite - Invite friends\nJoin channel: {channel_url}",
        "zh": "\n本机器人可自动完成 SheerID 认证。\n\n快速开始：\n/about - 了解机器人功能\n/balance - 查看积分余额\n/help - 查看完整命令列表\n\n获取更多积分：\n/qd - 每日签到\n/invite - 邀请好友\n加入频道：{channel_url}",
        "fa": "\nاین ربات می‌تواند تأییدیه‌های SheerID را به صورت خودکار انجام دهد.\n\nشروع سریع:\n/about - درباره ربات\n/balance - بررسی موجودی\n/help - لیست کامل دستورات\n\nدریافت امتیاز بیشتر:\n/qd - حضور و غیاب روزانه\n/invite - دعوت دوستان\nعضویت در کانال: {channel_url}",
        "ar": "\nيمكن لهذا البوت إكمال عمليات التحقق من SheerID تلقائيًا.\n\nالبداية السريعة:\n/about - حول البوت\n/balance - التحقق من الرصيد\n/help - قائمة الأوامر الكاملة\n\nاحصل على المزيد من النقاط:\n/qd - تسجيل الحضور اليومي\n/invite - دعوة الأصدقاء\nانضم إلى القناة: {channel_url}",
    },
    "welcome_back": {
        "en": "Welcome back, {full_name}!\nYou are already registered.\nSend /help to see available commands.",
        "zh": "欢迎回来，{full_name}！\n您已经初始化过了。\n发送 /help 查看可用命令。",
        "fa": "خوش آمدید، {full_name}!\nشما قبلاً ثبت نام کرده‌اید.\nبرای مشاهده دستورات موجود /help را ارسال کنید.",
        "ar": "أهلاً بك مجدداً، {full_name}!\nأنت مسجل بالفعل.\nأرسل /help لرؤية الأوامر المتاحة.",
    },
    "registration_failed": {
        "en": "Registration failed, please try again later.",
        "zh": "注册失败，请稍后重试。",
        "fa": "ثبت نام ناموفق بود، لطفاً بعداً دوباره تلاش کنید.",
        "ar": "فشل التسجيل، يرجى المحاولة مرة أخرى لاحقاً.",
    },
    "blocked_user": {
        "en": "You have been blocked and cannot use this feature.",
        "zh": "您已被拉黑，无法使用此功能。",
        "fa": "شما مسدود شده‌اید و نمی‌توانید از این ویژگی استفاده کنید.",
        "ar": "تم حظرك ولا يمكنك استخدام هذه الميزة.",
    },
    "not_registered": {
        "en": "Please register with /start first.",
        "zh": "请先使用 /start 注册。",
        "fa": "لطفاً ابتدا با /start ثبت نام کنید.",
        "ar": "يرجى التسجيل باستخدام /start أولاً.",
    },

    # About
    "about_message": {
        "en": "🤖 SheerID Auto Verification Bot\n\nFeatures:\n- Auto complete SheerID Student/Teacher verification\n- Supports Gemini One Pro, ChatGPT Teacher K12, Spotify Student, YouTube Student, Bolt.new Teacher\n\nPoints:\n- Register: +1 point\n- Daily Check-in: +1 point\n- Invite Friend: +2 points/person\n- Use Card Key\n- Join Channel: {channel_url}\n\nUsage:\n1. Start verification on the website and copy the full link\n2. Send /verify, /verify2, /verify3, /verify4 or /verify5 with the link\n3. Wait for processing\n4. For Bolt.new, use /getV4Code <verification_id> if needed\n\nMore commands: /help",
        "zh": "🤖 SheerID 自动认证机器人\n\n功能介绍:\n- 自动完成 SheerID 学生/教师认证\n- 支持 Gemini One Pro、ChatGPT Teacher K12、Spotify Student、YouTube Student、Bolt.new Teacher 认证\n\n积分获取:\n- 注册赠送 1 积分\n- 每日签到 +1 积分\n- 邀请好友 +2 积分/人\n- 使用卡密（按卡密规则）\n- 加入频道：{channel_url}\n\n使用方法:\n1. 在网页开始认证并复制完整的验证链接\n2. 发送 /verify、/verify2、/verify3、/verify4 或 /verify5 携带该链接\n3. 等待处理并查看结果\n4. Bolt.new 认证会自动获取认证码，如需手动查询使用 /getV4Code <verification_id>\n\n更多命令请发送 /help",
        "fa": "🤖 ربات تأیید خودکار SheerID\n\nویژگی‌ها:\n- تکمیل خودکار تأیید دانشجو/معلم SheerID\n- پشتیبانی از Gemini One Pro, ChatGPT Teacher K12, Spotify Student, YouTube Student, Bolt.new Teacher\n\nامتیازات:\n- ثبت نام: +۱ امتیاز\n- حضور و غیاب روزانه: +۱ امتیاز\n- دعوت دوست: +۲ امتیاز/نفر\n- استفاده از کلید کارت\n- عضویت در کانال: {channel_url}\n\nنحوه استفاده:\n۱. تأیید را در وب‌سایت شروع کنید و لینک کامل را کپی کنید\n۲. ارسال /verify, /verify2, /verify3, /verify4 یا /verify5 به همراه لینک\n۳. منتظر پردازش بمانید\n۴. برای Bolt.new در صورت نیاز از /getV4Code <verification_id> استفاده کنید\n\nدستورات بیشتر: /help",
        "ar": "🤖 بوت التحقق التلقائي SheerID\n\nالميزات:\n- إكمال تلقائي للتحقق من طالب/معلم SheerID\n- يدعم Gemini One Pro, ChatGPT Teacher K12, Spotify Student, YouTube Student, Bolt.new Teacher\n\nالنقاط:\n- التسجيل: +1 نقطة\n- تسجيل الحضور اليومي: +1 نقطة\n- دعوة صديق: +2 نقطة/شخص\n- استخدام مفتاح البطاقة\n- انضم إلى القناة: {channel_url}\n\nالاستخدام:\n1. ابدأ التحقق على الموقع وانسخ الرابط الكامل\n2. أرسل /verify, /verify2, /verify3, /verify4 أو /verify5 مع الرابط\n3. انتظر المعالجة\n4. بالنسبة لـ Bolt.new، استخدم /getV4Code <verification_id> إذا لزم الأمر\n\nالمزيد من الأوامر: /help",
    },

    # Help
    "help_title": {
        "en": "📖 SheerID Auto Verification Bot - Help",
        "zh": "📖 SheerID 自动认证机器人 - 帮助",
        "fa": "📖 ربات تأیید خودکار SheerID - راهنما",
        "ar": "📖 بوت التحقق التلقائي SheerID - مساعدة",
    },
    "help_user_commands": {
        "en": "User Commands:\n/start - Start (Register)\n/about - About Bot\n/balance - Check Balance\n/qd - Daily Check-in (+1 point)\n/invite - Generate Invite Link (+2 points/person)\n/use <key> - Use Card Key\n/language - Change Language\n",
        "zh": "用户命令:\n/start - 开始使用（注册）\n/about - 了解机器人功能\n/balance - 查看积分余额\n/qd - 每日签到（+1积分）\n/invite - 生成邀请链接（+2积分/人）\n/use <卡密> - 使用卡密兑换积分\n/language - 切换语言\n",
        "fa": "دستورات کاربر:\n/start - شروع (ثبت نام)\n/about - درباره ربات\n/balance - بررسی موجودی\n/qd - حضور و غیاب روزانه (+۱ امتیاز)\n/invite - ایجاد لینک دعوت (+۲ امتیاز/نفر)\n/use <key> - استفاده از کلید کارت\n/language - تغییر زبان\n",
        "ar": "أوامر المستخدم:\n/start - ابدأ (تسجيل)\n/about - حول البوت\n/balance - التحقق من الرصيد\n/qd - تسجيل الحضور اليومي (+1 نقطة)\n/invite - إنشاء رابط دعوة (+2 نقطة/شخص)\n/use <key> - استخدام مفتاح البطاقة\n/language - تغيير اللغة\n",
    },
    "help_verify_commands": {
        "en": "/verify <link> - Gemini One Pro (-{cost} points)\n/verify2 <link> - ChatGPT Teacher K12 (-{cost} points)\n/verify3 <link> - Spotify Student (-{cost} points)\n/verify4 <link> - Bolt.new Teacher (-{cost} points)\n/verify5 <link> - YouTube Student Premium (-{cost} points)\n/getV4Code <id> - Get Bolt.new Code\n/help - Show this help\nFailed? Check: {help_url}",
        "zh": "/verify <链接> - Gemini One Pro 认证（-{cost}积分）\n/verify2 <链接> - ChatGPT Teacher K12 认证（-{cost}积分）\n/verify3 <链接> - Spotify Student 认证（-{cost}积分）\n/verify4 <链接> - Bolt.new Teacher 认证（-{cost}积分）\n/verify5 <链接> - YouTube Student Premium 认证（-{cost}积分）\n/getV4Code <verification_id> - 获取 Bolt.new 认证码\n/help - 查看此帮助信息\n认证失败查看：{help_url}",
        "fa": "/verify <link> - Gemini One Pro (-{cost} امتیاز)\n/verify2 <link> - ChatGPT Teacher K12 (-{cost} امتیاز)\n/verify3 <link> - Spotify Student (-{cost} امتیاز)\n/verify4 <link> - Bolt.new Teacher (-{cost} امتیاز)\n/verify5 <link> - YouTube Student Premium (-{cost} امتیاز)\n/getV4Code <id> - دریافت کد Bolt.new\n/help - نمایش این راهنما\nناموفق؟ بررسی کنید: {help_url}",
        "ar": "/verify <link> - Gemini One Pro (-{cost} نقطة)\n/verify2 <link> - ChatGPT Teacher K12 (-{cost} نقطة)\n/verify3 <link> - Spotify Student (-{cost} نقطة)\n/verify4 <link> - Bolt.new Teacher (-{cost} نقطة)\n/verify5 <link> - YouTube Student Premium (-{cost} نقطة)\n/getV4Code <id> - الحصول على رمز Bolt.new\n/help - عرض هذه المساعدة\nفشل؟ تحقق: {help_url}",
    },

    # Balance
    "balance_title": {
        "en": "💰 Balance",
        "zh": "💰 积分余额",
        "fa": "💰 موجودی",
        "ar": "💰 الرصيد",
    },
    "current_balance": {
        "en": "Current Balance: {balance} points",
        "zh": "当前积分：{balance} 分",
        "fa": "موجودی فعلی: {balance} امتیاز",
        "ar": "الرصيد الحالي: {balance} نقطة",
    },
    "insufficient_balance": {
        "en": "Insufficient balance! Need {cost} points, current {balance} points.\n\nGet points:\n- Daily Check-in /qd\n- Invite Friends /invite\n- Use Card Key /use <key>",
        "zh": "积分不足！需要 {cost} 积分，当前 {balance} 积分。\n\n获取积分方式:\n- 每日签到 /qd\n- 邀请好友 /invite\n- 使用卡密 /use <卡密>",
        "fa": "موجودی کافی نیست! نیاز به {cost} امتیاز، موجودی فعلی {balance} امتیاز.\n\nدریافت امتیاز:\n- حضور و غیاب روزانه /qd\n- دعوت دوستان /invite\n- استفاده از کلید کارت /use <key>",
        "ar": "الرصيد غير كافٍ! تحتاج إلى {cost} نقطة، الرصيد الحالي {balance} نقطة.\n\nاحصل على النقاط:\n- تسجيل الحضور اليومي /qd\n- دعوة الأصدقاء /invite\n- استخدام مفتاح البطاقة /use <key>",
    },

    # Checkin
    "checkin_already": {
        "en": "❌ You have already checked in today. Come back tomorrow.",
        "zh": "❌ 今天已经签到过了，明天再来吧。",
        "fa": "❌ شما امروز حضور و غیاب کرده‌اید. فردا برگردید.",
        "ar": "❌ لقد قمت بتسجيل الحضور اليوم بالفعل. عد غداً.",
    },
    "checkin_success": {
        "en": "✅ Check-in successful!\nPoints earned: +1\nCurrent Balance: {balance} points",
        "zh": "✅ 签到成功！\n获得积分：+1\n当前积分：{balance} 分",
        "fa": "✅ حضور و غیاب موفق بود!\nامتیاز کسب شده: +۱\nموجودی فعلی: {balance} امتیاز",
        "ar": "✅ تم تسجيل الحضور بنجاح!\nالنقاط المكتسبة: +1\nالرصيد الحالي: {balance} نقطة",
    },

    # Invite
    "invite_message": {
        "en": "🎁 Your invite link:\n{invite_link}\n\nEarn 2 points for every successful registration.",
        "zh": "🎁 您的专属邀请链接：\n{invite_link}\n\n每邀请 1 位成功注册，您将获得 2 积分。",
        "fa": "🎁 لینک دعوت شما:\n{invite_link}\n\nبرای هر ثبت نام موفق ۲ امتیاز کسب کنید.",
        "ar": "🎁 رابط الدعوة الخاص بك:\n{invite_link}\n\nاحصل على نقطتين لكل تسجيل ناجح.",
    },

    # Use Key
    "use_key_usage": {
        "en": "Usage: /use <key>\nExample: /use wandouyu",
        "zh": "使用方法: /use <卡密>\n\n示例: /use wandouyu",
        "fa": "نحوه استفاده: /use <key>\nمثال: /use wandouyu",
        "ar": "الاستخدام: /use <key>\nمثال: /use wandouyu",
    },
    "key_not_found": {
        "en": "Key not found, please check and try again.",
        "zh": "卡密不存在，请检查后重试。",
        "fa": "کلید پیدا نشد، لطفاً بررسی و دوباره تلاش کنید.",
        "ar": "المفتاح غير موجود، يرجى التحقق والمحاولة مرة أخرى.",
    },
    "key_limit_reached": {
        "en": "This key has reached its usage limit.",
        "zh": "该卡密已达到使用次数上限。",
        "fa": "این کلید به سقف استفاده خود رسیده است.",
        "ar": "لقد وصل هذا المفتاح إلى الحد الأقصى للاستخدام.",
    },
    "key_expired": {
        "en": "This key has expired.",
        "zh": "该卡密已过期。",
        "fa": "این کلید منقضی شده است.",
        "ar": "لقد انتهت صلاحية هذا المفتاح.",
    },
    "key_already_used": {
        "en": "You have already used this key.",
        "zh": "您已经使用过该卡密。",
        "fa": "شما قبلاً از این کلید استفاده کرده‌اید.",
        "ar": "لقد استخدمت هذا المفتاح بالفعل.",
    },
    "key_success": {
        "en": "Key used successfully!\nPoints earned: {amount}\nCurrent Balance: {balance}",
        "zh": "卡密使用成功！\n获得积分：{amount}\n当前积分：{balance}",
        "fa": "کلید با موفقیت استفاده شد!\nامتیاز کسب شده: {amount}\nموجودی فعلی: {balance}",
        "ar": "تم استخدام المفتاح بنجاح!\nالنقاط المكتسبة: {amount}\nالرصيد الحالي: {balance}",
    },

    # Verify Usage
    "verify_usage": {
        "en": "Usage: {command} <SheerID Link>\n\nExample:\n{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\nHow to get link:\n1. Visit {service_name} verification page\n2. Start verification process\n3. Copy the full URL from address bar\n4. Submit using {command}",
        "zh": "使用方法: {command} <SheerID链接>\n\n示例:\n{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\n获取验证链接:\n1. 访问 {service_name} 认证页面\n2. 开始认证流程\n3. 复制浏览器地址栏中的完整 URL\n4. 使用 {command} 命令提交",
        "fa": "نحوه استفاده: {command} <لینک SheerID>\n\nمثال:\n{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\nنحوه دریافت لینک:\n۱. به صفحه تأیید {service_name} بروید\n۲. فرآیند تأیید را شروع کنید\n۳. آدرس کامل را از نوار آدرس کپی کنید\n۴. با استفاده از {command} ارسال کنید",
        "ar": "الاستخدام: {command} <رابط SheerID>\n\nمثال:\n{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\nكيفية الحصول على الرابط:\n1. قم بزيارة صفحة التحقق {service_name}\n2. ابدأ عملية التحقق\n3. انسخ عنوان URL الكامل من شريط العناوين\n4. أرسل باستخدام {command}",
    },
    "invalid_link": {
        "en": "Invalid SheerID link, please check and try again.",
        "zh": "无效的 SheerID 链接，请检查后重试。",
        "fa": "لینک SheerID نامعتبر است، لطفاً بررسی و دوباره تلاش کنید.",
        "ar": "رابط SheerID غير صالح، يرجى التحقق والمحاولة مرة أخرى.",
    },
    "deduct_failed": {
        "en": "Failed to deduct points, please try again later.",
        "zh": "扣除积分失败，请稍后重试。",
        "fa": "کسر امتیاز ناموفق بود، لطفاً بعداً دوباره تلاش کنید.",
        "ar": "فشل خصم النقاط، يرجى المحاولة مرة أخرى لاحقاً.",
    },

    # Verification Process
    "verify_start": {
        "en": "Starting {service_name} verification...\nVerification ID: {verification_id}\nDeducted {cost} points\n\nPlease wait, this may take 1-2 minutes...",
        "zh": "开始处理 {service_name} 认证...\n验证ID: {verification_id}\n已扣除 {cost} 积分\n\n请稍候，这可能需要 1-2 分钟...",
        "fa": "شروع تأیید {service_name}...\nشناسه تأیید: {verification_id}\n{cost} امتیاز کسر شد\n\nلطفاً صبر کنید، این ممکن است ۱-۲ دقیقه طول بکشد...",
        "ar": "بدء التحقق من {service_name}...\nمعرف التحقق: {verification_id}\nتم خصم {cost} نقطة\n\nيرجى الانتظار، قد يستغرق هذا 1-2 دقيقة...",
    },
    "verify_start_detailed": {
        "en": "🎵 Starting {service_name} verification...\nDeducted {cost} points\n\n📝 Generating student info...\n🎨 Generating ID card PNG...\n📤 Submitting documents...",
        "zh": "🎵 开始处理 {service_name} 认证...\n已扣除 {cost} 积分\n\n📝 正在生成学生信息...\n🎨 正在生成学生证 PNG...\n📤 正在提交文档...",
        "fa": "🎵 شروع تأیید {service_name}...\n{cost} امتیاز کسر شد\n\n📝 در حال تولید اطلاعات دانشجو...\n🎨 در حال تولید کارت شناسایی PNG...\n📤 در حال ارسال مدارک...",
        "ar": "🎵 بدء التحقق من {service_name}...\nتم خصم {cost} نقطة\n\n📝 جاري إنشاء معلومات الطالب...\n🎨 جاري إنشاء بطاقة الهوية PNG...\n📤 جاري تقديم المستندات...",
    },

    # Verification Result
    "verify_success": {
        "en": "✅ Verification Successful!\n\n",
        "zh": "✅ 认证成功！\n\n",
        "fa": "✅ تأیید موفقیت آمیز بود!\n\n",
        "ar": "✅ تم التحقق بنجاح!\n\n",
    },
    "verify_pending": {
        "en": "✨ Documents submitted, waiting for manual review.\n",
        "zh": "✨ 文档已提交，等待人工审核。\n",
        "fa": "✨ مدارک ارسال شد، در انتظار بررسی دستی.\n",
        "ar": "✨ تم تقديم المستندات، في انتظار المراجعة اليدوية.\n",
    },
    "verify_redirect": {
        "en": "🔗 Redirect Link:\n{url}",
        "zh": "🔗 跳转链接：\n{url}",
        "fa": "🔗 لینک تغییر مسیر:\n{url}",
        "ar": "🔗 رابط إعادة التوجيه:\n{url}",
    },
    "verify_failed": {
        "en": "❌ Verification Failed: {message}\n\nReturned {cost} points",
        "zh": "❌ 认证失败：{message}\n\n已退回 {cost} 积分",
        "fa": "❌ تأیید ناموفق: {message}\n\n{cost} امتیاز برگشت داده شد",
        "ar": "❌ فشل التحقق: {message}\n\nتم استرداد {cost} نقطة",
    },
    "verify_error": {
        "en": "❌ Error during processing: {error}\n\nReturned {cost} points",
        "zh": "❌ 处理过程中出现错误：{error}\n\n已退回 {cost} 积分",
        "fa": "❌ خطا در پردازش: {error}\n\n{cost} امتیاز برگشت داده شد",
        "ar": "❌ حدث خطأ أثناء المعالجة: {error}\n\nتم استرداد {cost} نقطة",
    },

    # Bolt.new specific
    "bolt_start": {
        "en": "🚀 Starting Bolt.new Teacher verification...\nDeducted {cost} points\n\n📤 Submitting documents...",
        "zh": "🚀 开始处理 Bolt.new Teacher 认证...\n已扣除 {cost} 积分\n\n📤 正在提交文档...",
        "fa": "🚀 شروع تأیید معلم Bolt.new...\n{cost} امتیاز کسر شد\n\n📤 در حال ارسال مدارک...",
        "ar": "🚀 بدء التحقق من معلم Bolt.new...\nتم خصم {cost} نقطة\n\n📤 جاري تقديم المستندات...",
    },
    "bolt_doc_failed": {
        "en": "❌ Document submission failed: {message}\n\nReturned {cost} points",
        "zh": "❌ 文档提交失败：{message}\n\n已退回 {cost} 积分",
        "fa": "❌ ارسال مدارک ناموفق بود: {message}\n\n{cost} امتیاز برگشت داده شد",
        "ar": "❌ فشل تقديم المستند: {message}\n\nتم استرداد {cost} نقطة",
    },
    "bolt_submitted": {
        "en": "✅ Documents submitted!\n📋 Verification ID: `{vid}`\n\n🔍 Automatically retrieving reward code...\n(Wait up to 20s)",
        "zh": "✅ 文档已提交！\n📋 验证ID: `{vid}`\n\n🔍 正在自动获取认证码...\n（最多等待20秒）",
        "fa": "✅ مدارک ارسال شد!\n📋 شناسه تأیید: `{vid}`\n\n🔍 در حال بازیابی خودکار کد پاداش...\n(تا ۲۰ ثانیه صبر کنید)",
        "ar": "✅ تم تقديم المستندات!\n📋 معرف التحقق: `{vid}`\n\n🔍 جاري استرداد رمز المكافأة تلقائيًا...\n(انتظر حتى 20 ثانية)",
    },
    "bolt_success_code": {
        "en": "🎉 Verification Successful!\n\n✅ Documents submitted\n✅ Review passed\n✅ Code retrieved\n\n🎁 Reward Code: `{code}`\n",
        "zh": "🎉 认证成功！\n\n✅ 文档已提交\n✅ 审核已通过\n✅ 认证码已获取\n\n🎁 认证码: `{code}`\n",
        "fa": "🎉 تأیید موفقیت آمیز بود!\n\n✅ مدارک ارسال شد\n✅ بررسی انجام شد\n✅ کد دریافت شد\n\n🎁 کد پاداش: `{code}`\n",
        "ar": "🎉 تم التحقق بنجاح!\n\n✅ تم تقديم المستندات\n✅ تم اجتياز المراجعة\n✅ تم استرداد الرمز\n\n🎁 رمز المكافأة: `{code}`\n",
    },
    "bolt_pending_code": {
        "en": "✅ Documents submitted successfully!\n\n⏳ Reward code not yet generated (Review takes 1-5 mins)\n\n📋 Verification ID: `{vid}`\n\n💡 Check later with:\n`/getV4Code {vid}`\n\nNote: Points consumed, no extra cost for checking later.",
        "zh": "✅ 文档已提交成功！\n\n⏳ 认证码尚未生成（可能需要1-5分钟审核）\n\n📋 验证ID: `{vid}`\n\n💡 请稍后使用以下命令查询:\n`/getV4Code {vid}`\n\n注意：积分已消耗，稍后查询无需再付费",
        "fa": "✅ مدارک با موفقیت ارسال شد!\n\n⏳ کد پاداش هنوز تولید نشده است (بررسی ۱-۵ دقیقه طول می‌کشد)\n\n📋 شناسه تأیید: `{vid}`\n\n💡 بعداً بررسی کنید با:\n`/getV4Code {vid}`\n\nنکته: امتیاز مصرف شده، بدون هزینه اضافی برای بررسی بعدی.",
        "ar": "✅ تم تقديم المستندات بنجاح!\n\n⏳ لم يتم إنشاء رمز المكافأة بعد (تستغرق المراجعة 1-5 دقائق)\n\n📋 معرف التحقق: `{vid}`\n\n💡 تحقق لاحقًا باستخدام:\n`/getV4Code {vid}`\n\nملاحظة: تم استهلاك النقاط، لا توجد تكلفة إضافية للتحقق لاحقًا.",
    },
    "bolt_code_usage": {
        "en": "Usage: /getV4Code <verification_id>\n\nExample: /getV4Code 6929436b50d7dc18638890d0\n\nverification_id is returned after using /verify4.",
        "zh": "使用方法: /getV4Code <verification_id>\n\n示例: /getV4Code 6929436b50d7dc18638890d0\n\nverification_id 在使用 /verify4 命令后会返回给您。",
        "fa": "نحوه استفاده: /getV4Code <verification_id>\n\nمثال: /getV4Code 6929436b50d7dc18638890d0\n\nverification_id پس از استفاده از /verify4 بازگردانده می‌شود.",
        "ar": "الاستخدام: /getV4Code <verification_id>\n\nمثال: /getV4Code 6929436b50d7dc18638890d0\n\nيتم إرجاع verification_id بعد استخدام /verify4.",
    },
    "bolt_query_wait": {
        "en": "🔍 Querying reward code, please wait...",
        "zh": "🔍 正在查询认证码，请稍候...",
        "fa": "🔍 در حال پرس و جو برای کد پاداش، لطفاً صبر کنید...",
        "ar": "🔍 جاري الاستعلام عن رمز المكافأة، يرجى الانتظار...",
    },
    "bolt_query_failed": {
        "en": "❌ Query failed, status code: {status}\n\nPlease try again later.",
        "zh": "❌ 查询失败，状态码：{status}\n\n请稍后重试或联系管理员。",
        "fa": "❌ پرس و جو ناموفق بود، کد وضعیت: {status}\n\nلطفاً بعداً دوباره تلاش کنید.",
        "ar": "❌ فشل الاستعلام، رمز الحالة: {status}\n\nيرجى المحاولة مرة أخرى لاحقاً.",
    },
    "bolt_query_pending": {
        "en": "⏳ Verification is still pending, please try again later.\n\nUsually takes 1-5 minutes.",
        "zh": "⏳ 认证仍在审核中，请稍后再试。\n\n通常需要 1-5 分钟，请耐心等待。",
        "fa": "⏳ تأیید هنوز در حال انجام است، لطفاً بعداً دوباره تلاش کنید.\n\nمعمولاً ۱-۵ دقیقه طول می‌کشد.",
        "ar": "⏳ التحقق لا يزال معلقاً، يرجى المحاولة مرة أخرى لاحقاً.\n\nتستغرق عادة 1-5 دقائق.",
    },
    "bolt_query_no_code": {
        "en": "⚠️ Current status: {status}\n\nReward code not yet generated, please try again later.",
        "zh": "⚠️ 当前状态：{status}\n\n认证码尚未生成，请稍后重试。",
        "fa": "⚠️ وضعیت فعلی: {status}\n\nکد پاداش هنوز تولید نشده است، لطفاً بعداً دوباره تلاش کنید.",
        "ar": "⚠️ الحالة الحالية: {status}\n\nلم يتم إنشاء رمز المكافأة بعد، يرجى المحاولة مرة أخرى لاحقاً.",
    },

    # Language
    "language_select": {
        "en": "Please select your language:",
        "zh": "请选择您的语言：",
        "fa": "لطفاً زبان خود را انتخاب کنید:",
        "ar": "الرجاء اختيار لغتك:",
    },
    "language_set": {
        "en": "Language set to English.",
        "zh": "语言已设置为中文。",
        "fa": "زبان روی فارسی تنظیم شد.",
        "ar": "تم تعيين اللغة إلى العربية.",
    },

    # Menu Buttons
    "menu_verify": {
        "en": "🔐 Verify",
        "zh": "🔐 认证",
        "fa": "🔐 تأیید",
        "ar": "🔐 تحقق",
    },
    "menu_balance": {
        "en": "💰 Balance",
        "zh": "💰 余额",
        "fa": "💰 موجودی",
        "ar": "💰 الرصيد",
    },
    "menu_checkin": {
        "en": "📅 Daily Check-in",
        "zh": "📅 每日签到",
        "fa": "📅 حضور و غیاب",
        "ar": "📅 تسجيل الحضور",
    },
    "menu_invite": {
        "en": "🤝 Invite",
        "zh": "🤝 邀请",
        "fa": "🤝 دعوت",
        "ar": "🤝 دعوة",
    },
    "menu_help": {
        "en": "❓ Help",
        "zh": "❓ 帮助",
        "fa": "❓ راهنما",
        "ar": "❓ مساعدة",
    },
    "menu_language": {
        "en": "🌐 Language",
        "zh": "🌐 语言",
        "fa": "🌐 زبان",
        "ar": "🌐 اللغة",
    },
}

def get_text(key: str, lang: str = "en", **kwargs) -> str:
    """Get localized text"""
    if lang not in LANGUAGES:
        lang = DEFAULT_LANGUAGE

    # Fallback to English if translation missing
    translations = TRANSLATIONS.get(key, {})
    text = translations.get(lang)

    if text is None:
        text = translations.get(DEFAULT_LANGUAGE, "")

    if not text:
        return key

    try:
        return text.format(**kwargs)
    except KeyError as e:
        return text # Return unformatted text if key missing
