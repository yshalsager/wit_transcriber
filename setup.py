import os
import sys
from pathlib import Path
from shutil import copy

import cx_Freeze

__version__ = "1.0.0"
base = None
include_files = ["assets/chat-centered-text-duotone.ico"]

if sys.platform == "win32":
    base = "Win32GUI"
    os.environ["TCL_LIBRARY"] = r"PATH_TO_PYTHON\\tcl\\tcl8.6"
    os.environ["TK_LIBRARY"] = r"PATH_TO_PYTHON\\tcl\\tk8.6"
    path = Path(__file__).parent.resolve()
    if (path / "ffmpeg.exe").exists():
        include_files.append("ffmpeg.exe")
    build_path = path / "build" / "exe.win32-3.7"
    copy(r"PATH_TO_PYTHON\\DLLs\\tcl86t.dll", build_path)
    copy(r"PATH_TO_PYTHON\\DLLs\\tk86t.dll", build_path)

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
    name="Transcribe Arabic",
    description="تحويل الملفات الصوتية الي نصوص",
    version=__version__,
    executables=[
        cx_Freeze.Executable(
            "wit_transcriber/gui/main_window.py",
            base=base,
            icon="assets/chat-centered-text-duotone.ico",
            shortcutName="Transcribe Arabic",
            shortcutDir="DesktopFolder",
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
            "initial_target_dir": rf"[ProgramFilesFolder]\TranscribeArabic",
        },
        "bdist_mac": {
            "iconfile": "chat-centered-text-duotone.icns",
            "bundle_name": "TranscribeArabic",
        },
        "bdist_dmg": {
            "volume_label": "Install Transcribe Arabic",
            "applications_shortcut": True,
        },
    },
)
