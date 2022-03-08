# wit_transcriber

A mini command line tool to transcribe media files using [wit.ai](https://wit.ai)

[![GitHub release](https://img.shields.io/github/release/yshalsager/wit_transcriber.svg)](https://github.com/yshalsager/wit_transcriber/releases/)

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![PayPal](https://img.shields.io/badge/PayPal-Donate-00457C?style=flat&labelColor=00457C&logo=PayPal&logoColor=white&link=https://www.paypal.me/yshalsager)](https://www.paypal.me/yshalsager)
[![Patreon](https://img.shields.io/badge/Patreon-Support-F96854?style=flat&labelColor=F96854&logo=Patreon&logoColor=white&link=https://www.patreon.com/XiaomiFirmwareUpdater)](https://www.patreon.com/XiaomiFirmwareUpdater)
[![Liberapay](https://img.shields.io/badge/Liberapay-Support-F6C915?style=flat&labelColor=F6C915&logo=Liberapay&logoColor=white&link=https://liberapay.com/yshalsager)](https://liberapay.com/yshalsager)

## Configuring Wit.ai

- Open [wit.ai](https://wit.ai/) and sign with Facebook account.
- Go to [wit.ai/apps](https://wit.ai/apps) and click on New App.
- Choose a name and select a language, set the app visibility to private, then press Create.
- Go to Management > Settings (`https://wit.ai/apps/<App ID>/settings`).
- Under the Client Access Token section click on the token to copy it, this is the API key.

## Usage

**Note**: ffmpeg must be installed!

Copy config example file to `config.json` and add required languages API keys you got from the previous step.

```bash
usage: wit_transcriber.py [-h] -i INPUT [-o OUTPUT] [-c CONFIG] [-x CONNECTIONS] [-l LANG] [-v]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path of media file to be transcribed.
  -o OUTPUT, --output OUTPUT
                        Path of output file.
  -c CONFIG, --config CONFIG
                        Path of config file.
  -x CONNECTIONS, --connections CONNECTIONS
                        Number of API connections limit.
  -l LANG, --lang LANG  Language to use.
  -v, --verbose         Print API responses.
```

---

# أداة التفريغ النصي بواسطة wit.ai

أداة صغيرة لتفريغ الصوتيات عبر [wit.ai](https://wit.ai).

## إعداد Wit.ai

- افتح [wit.ai](https://wit.ai/) وسجل الدخول بحساب فيس بوك.
- افتح [wit.ai/apps](https://wit.ai/apps) واضغط على New App لإنشاء تطبيق جديد.
- اختر اسمًا للتطبيق واختر لغةَ ثم عدل إعدادات ظهور التطبيق إلى خاص واضغط إنشاء.
- افتح قسم اﻹدارة ثم اﻹعدادات Management > Settings (`https://wit.ai/apps/<App ID>/settings`).
- أسفل قسم Client Access Token section ستجد مفتاح استخدام الواجهة البرمجية، انسخه لتستخدمه في الخطوة التالية.

## الاستخدام

انسخ ملف config example إلى ملف باسم `config.json` ثم أضف مفاتيح استخدام الواجهة البرمجية الخاصة باللغات المطلوبة.

### تشغيل اﻷداة على ويندوز

- حمل أحدث نسخة من الملف التنفيذي للأداة من [هنا](https://github.com/yshalsager/wit_transcriber/releases/latest).
- حمل ملفات ffmpeg إذا لم يكن مثبتا عندك من [هنا](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z) وفك الضغط عن الملف ثم انقل `ffmpeg.exe` و `ffprobe.exe` إلى نفس المجلد الذي به الأداة.
- شغل الملف التنفيذي عبر سطر/موجه اﻷوامر مع استبدال كلمة filename باسم الملف المراد تفريغه.

```powershell
./wit_transcriber.exe -i filename
```
