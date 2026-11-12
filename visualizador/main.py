"""ponto de entrada do G-Path"""
import sys, traceback, json

from core.i18n import set_language, tr
import config

from PySide6.QtCore import QLocale, Qt
from PySide6.QtWidgets import QApplication, QMessageBox

from ui.main_window import MainWindow

def _install_excepthook() -> None:

    def handle(exc_type, exc_value, exc_tb):
        detail = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print(detail, file=sys.stderr)
        box = QMessageBox(
            QMessageBox.Icon.Critical,
            tr("unexpected_error_title"),
            tr("unexpected_error_text").format(err=exc_value),
        )
        box.setDetailedText(detail)
        box.exec()

    sys.excepthook = handle

def _default_language() -> str:
    """primeiro uso, sem settings.json salvo: segue o idioma do sistema."""
    return "pt_BR" if QLocale.system().name().startswith("pt") else "en"

def _load_saved_language() -> str:
    try:
        data = json.loads(config.SETTINGS_FILE.read_text(encoding="utf-8"))
        return data.get("language") or _default_language()
    except (FileNotFoundError, json.JSONDecodeError):
        return _default_language()

def main() -> int:
    set_language(_load_saved_language())
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    # a lista dos combos abre com o fade do próprio programa, não com o deslize do sistema
    app.setEffectEnabled(Qt.UIEffect.UI_AnimateCombo, False)
    _install_excepthook()
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())