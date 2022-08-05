from awesometkinter.bidirender import render_text


def _text(platform: str, text: str) -> str:
    """A helper function to get text in correct direction based on OS."""
    return render_text(text) if platform != "Windows" else text
