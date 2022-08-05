pyinstaller-cli:
		pyinstaller -F wit_transcriber/cli/app.py \
		--clean -y \
		--add-data="pyproject.toml:." \
		-n wit_transcriber
pyinstaller-gui:
		pyinstaller -F wit_transcriber/gui/app.py \
		--clean -y \
		--add-data="pyproject.toml:." \
		--windowed \
		-n wit_transcriber_gui
