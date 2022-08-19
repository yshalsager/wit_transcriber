import sys
from pathlib import Path
from typing import List

import cx_Freeze

__version__ = "1.0.0"
base = None
include_files: List[str] = []
ffmpeg_files: List[str] = ["ffmpeg.exe", "ffprobe.exe"]
    
if sys.platform == "win32":
    base = "Win32GUI"
    for file in ffmpeg_files:
        if (Path(__file__).parent / file).exists():
            include_files.append(file)

includes = ["tkinter"]
excludes = ["matplotlib", "sqlite3"]
packages = [
    "httpx",
    "http",
    "anyio",
    "traceback",
    "pydub",
    "asyncio",
    "traceback",
    "json",
    "re",
    "typing",
    "pathlib",
    "ratelimiter",
    "distutils",
]

cx_Freeze.setup(
    name="TranscribeArabic",
    description="تحويل الملفات الصوتية إلى نصوص",
    version=__version__,
    executables=[
        cx_Freeze.Executable(
            "wit_transcriber/gui/app.py",
            base=base,
            icon="assets/chat-centered-text-duotone.ico",
            shortcut_name="Transcribe Arabic",
            shortcut_dir="DesktopFolder",
        )
    ],
    options={
        "build_exe": {
            "packages": packages,
            "includes": includes,
            "include_files": include_files,
            "include_msvcr": True,
            "excludes": excludes,
        },
        "bdist_msi": {
            "upgrade_code": "{00EF338F-794D-3AB8-8CD6-2B0AB7541021}",
            "add_to_path": False,
            "initial_target_dir": r"[ProgramFilesFolder]\TranscribeArabic",
            "install_icon": "assets/chat-centered-text-duotone.ico",
        },
        "bdist_mac": {
            "iconfile": "assets/chat-centered-text-duotone.icns",
            "bundle_name": "TranscribeArabic",
        },
        "bdist_dmg": {
            "volume_label": "Install Transcribe Arabic",
            "applications_shortcut": True,
        },
    },
)
