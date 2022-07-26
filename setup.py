import os
import shutil
import sys
import cx_Freeze 

os.environ['TCL_LIBRARY'] = r'PATH_TO_PYTHON\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = r'PATH_TO_PYTHON\\tcl\\tk8.6'

__version__ = '1.0.0'
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

include_files = ['ffmpeg.exe','main.ico']
includes = ['tkinter']
excludes = ['matplotlib', 'sqlite3']
packages = ['httpx','http','anyio', 'traceback', 'pydub','asyncio','traceback','json','re','typing','pathlib','ratelimiter','distutils']

bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % ('TranscribeArabic'),
    }

cx_Freeze.setup(
    name='Transcribe Arabic',
    description='تحويل الملفات الصوتية الي نصوص',
    version=__version__,
    executables=[cx_Freeze.Executable('application.py', base=base,icon='main.ico',shortcutName="Transcribe Arabic",
            shortcutDir="DesktopFolder",)],
    options = {
        'build_exe': {
            'packages': packages,
            'includes': includes,
            'include_files': include_files,
            'include_msvcr': True,
            'excludes': excludes,
        },
        'bdist_msi':{
            'upgrade_code': '{00EF338F-794D-3AB8-8CD6-2B0AB7541021}',
            'add_to_path': False,
            'initial_target_dir': r'[ProgramFilesFolder]\%s' % ('TranscribeArabic'),
    }},
)

path = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
build_path = os.path.join(path, 'build', 'exe.win32-3.7')
shutil.copy(r'PATH_TO_PYTHON\\DLLs\\tcl86t.dll', build_path)
shutil.copy(r'PATH_TO_PYTHON\\DLLs\\tk86t.dll', build_path)
