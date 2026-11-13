# --- tokens de design ---------------------------------------------------

SURFACE_0 = "#0d0e12"   # fundo da janela
SURFACE_1 = "#17191f"   # painéis (cartões, barra de reprodução, editor...)
SURFACE_2 = "#1f222a"   # elementos dentro de painéis (inputs, itens de lista)
SURFACE_3 = "#282c36"   # hover / destaque leve
BORDER = "#2c303b"
BORDER_STRONG = "#3a3f4b"

TEXT_PRIMARY = "#f2f3f5"
TEXT_SECONDARY = "#9aa3b2"
TEXT_MUTED = "#767c8a"

ACCENT = "#b85a26"
ACCENT_HOVER = "#cf6f36"
ACCENT_PRESSED = "#97471b"
ACCENT_SOFT = "#3b2c29"   # fundo de estado ativo/selecionado (laranja 18% sobre SURFACE_2)
ACCENT_TEXT = "#e8894f"   # texto/ícone laranja sobre fundos escuros
ON_ACCENT = "#ffffff"   # cor de texto/ícone sobre fundo ACCENT

SUCCESS = "#30d158"
ERROR_COLOR = "#ff6b6b"
WARNING_COLOR = "#f0b429"

RADIUS_SM = "6px"
RADIUS_MD = "8px"
RADIUS_LG = "12px"

SPACE_XXS = 2
SPACE_XS = 6
SPACE_SM = 8
SPACE_MD = 10
SPACE_LG = 12
SPACE_XL = 14
SPACE_XXL = 16

FONT_FAMILY = "'Segoe UI Variable Display', 'Segoe UI', sans-serif"

FONT_MONO = "Consolas, 'Cascadia Mono', 'DejaVu Sans Mono', monospace"
FONT_CAPTION = "11px"
FONT_SMALL = "12px"
FONT_BODY = "13px"
FONT_VALUE = "16px"
FONT_TITLE = "24px"
WEIGHT_REGULAR = "400"
WEIGHT_STRONG = "600"

# --- cores usadas no viewport 3D (full OpenGL, sem QSS) -----------------------

BACKGROUND = SURFACE_0
GRID_COLOR = (70, 75, 85, 255)

DIM_CUT = (0.2, 0.5, 0.7, 0.35)
BRIGHT_CUT = (0.2, 0.8, 1.0, 1.0)
DIM_RAPID = (1.0, 0.35, 0.35, 0.4)
BRIGHT_RAPID = (1.0, 0.35, 0.35, 0.8)
HEAD_COLOR = (1.0, 0.85, 0.2, 1.0)
ARC_HEAD_COLOR = (1.0, 0.45, 0.1, 1.0)
TORCH_COLOR = (0.55, 0.57, 0.62, 1.0)
WIRE_COLOR = (0.95, 0.95, 0.95, 1.0)
CUT_DEPTH_ALPHA = 0.35
DEPTH_STOPS = (
    (0.25, 0.5, 1.0),
    (0.3, 0.9, 0.7),
    (1.0, 0.85, 0.2),
)

# --- cores específicas do editor de código (gutter, linha atual, linha em execução) ---

EDITOR_TEXT = "#d7dce3"
EDITOR_GUTTER_BG = "#191b21"
EDITOR_GUTTER_TEXT = "#555c6b"
EDITOR_CURRENT_LINE_BG = "#23262f"
EDITOR_RUNNING_LINE_BG = "#3a2f12"
SYNTAX_LABEL = "#c792ea"      # rótulo O1000
SYNTAX_G_CODE = "#82aaff"     # G1, G90...
SYNTAX_M_CODE = "#f78c6c"     # M8, M98...
SYNTAX_AXIS = "#c3e88d"       # X10, Z-5...
SYNTAX_PARAM = "#ffcb6b"      # F400, S1200, P1000, L8
SYNTAX_VARIABLE = "#f07178"   # #1, #5
SYNTAX_NUMBER = "#89ddff"     # números soltos
SYNTAX_COMMENT = "#5c6370"

# --- folha de estilo ------------------------------------------------------

DARK_QSS = f"""
QMainWindow {{ background: {SURFACE_0}; }}
QWidget#central {{ background: {SURFACE_0}; }}
QMenuBar {{ background: {SURFACE_0}; color: {TEXT_PRIMARY}; padding: 2px 4px; }}
QMenuBar::item {{ background: transparent; padding: 4px 10px; border-radius: {RADIUS_SM}; }}
QMenuBar::item:selected {{ background: {SURFACE_3}; }}
QMenuBar::item:pressed {{ background: {SURFACE_2}; }}

QMenu {{
    background: {SURFACE_2}; color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_STRONG}; border-radius: {RADIUS_MD}; padding: 4px;
}}
QMenu::item {{ padding: 6px 28px 6px 10px; border-radius: {RADIUS_SM}; }}
QMenu::item:selected {{ background: {SURFACE_3}; }}
QMenu::item:disabled {{ color: {TEXT_MUTED}; }}
QMenu::icon {{ padding-left: 6px; }}
QMenu::separator {{ height: 1px; background: {BORDER}; margin: 4px 8px; }}
QDialog {{ background: {SURFACE_0}; }}
QDialog QLabel {{ color: {TEXT_PRIMARY}; }}

QLabel {{ color: {TEXT_PRIMARY}; background: transparent; font-family: {FONT_FAMILY}; font-size: {FONT_BODY}; }}
QLabel#fileLabel {{ color: {TEXT_SECONDARY}; }}
QLabel#profileLabel {{ color: {TEXT_SECONDARY}; font-weight: {WEIGHT_STRONG}; }}

QPushButton {{
    background: {SURFACE_2}; color: {TEXT_PRIMARY}; font-family: {FONT_FAMILY};
    border: none; border-radius: {RADIUS_MD}; padding: 7px 14px; font-weight: {WEIGHT_REGULAR};
}}
QPushButton:hover {{ background: {SURFACE_3}; }}
QPushButton:pressed {{ background: {SURFACE_1}; }}
QPushButton:disabled {{ color: {TEXT_MUTED}; }}
QPushButton:focus {{ border: 1px solid {ACCENT}; }}

QPushButton#play {{
    background: {ACCENT}; border-radius: 20px; padding: 0; font-size: {FONT_VALUE};
}}
QPushButton#play:hover {{ background: {ACCENT_HOVER}; }}
QPushButton#play:pressed {{ background: {ACCENT_PRESSED}; }}
QPushButton#play:disabled {{ background: {SURFACE_3}; }}

QPushButton#transport {{ background: transparent; border-radius: 17px; padding: 0; }}
QPushButton#transport:hover {{ background: {SURFACE_3}; }}
QPushButton#transport:pressed {{ background: {SURFACE_1}; }}

QPushButton#preset {{ padding: 3px 10px; font-size: {FONT_SMALL}; border-radius: {RADIUS_SM}; background: {SURFACE_2}; }}
QPushButton#preset:hover {{ background: {SURFACE_3}; }}

QFrame#playbar {{ background: {SURFACE_1}; border: none; border-radius: {RADIUS_LG}; }}

QLabel#timeLabel {{ color: {TEXT_PRIMARY}; font-family: {FONT_MONO}; font-size: {FONT_SMALL}; min-width: 44px; }}
QLabel#timeLabelMuted {{ color: {TEXT_SECONDARY}; font-family: {FONT_MONO}; font-size: {FONT_SMALL}; min-width: 44px; }}
QLabel#playerMessage {{ color: {TEXT_SECONDARY}; font-size: {FONT_SMALL}; }}

QFrame#suggestion {{ background: {SURFACE_1}; border: 1px solid {BORDER_STRONG}; border-radius: {RADIUS_MD}; }}
QLabel#suggestionText {{ color: {TEXT_PRIMARY}; font-size: {FONT_SMALL}; }}
QPushButton#suggestionButton {{ background: {ACCENT}; color: {ON_ACCENT}; padding: 4px 12px; font-size: {FONT_SMALL}; }}
QPushButton#suggestionButton:hover {{ background: {ACCENT_HOVER}; }}
QPushButton#suggestionClose {{ background: transparent; border: none; border-radius: {RADIUS_SM}; padding: 0; }}
QPushButton#suggestionClose:hover {{ background: {SURFACE_3}; }}

QFrame#dro {{ background: {SURFACE_1}; border: 1px solid {BORDER}; border-radius: {RADIUS_MD}; }}
QLabel#droName {{ color: {TEXT_SECONDARY}; font-family: {FONT_MONO}; font-size: {FONT_SMALL}; }}
QLabel#droValue {{ color: {TEXT_PRIMARY}; font-family: {FONT_MONO}; font-size: {FONT_SMALL}; min-width: 64px; }}

QLabel#chip {{
    color: {TEXT_SECONDARY}; background: {SURFACE_2}; border: 1px solid {BORDER};
    border-radius: {RADIUS_SM}; padding: 2px 8px; font-family: {FONT_MONO}; font-size: {FONT_SMALL};
}}
QToolButton#speedButton {{
    background: {SURFACE_2}; color: {TEXT_PRIMARY}; border: none; border-radius: {RADIUS_MD};
    padding: 5px 10px; font-family: {FONT_MONO}; font-size: {FONT_SMALL};
}}
QToolButton#speedButton:hover {{ background: {SURFACE_3}; }}
QToolButton#speedButton:disabled {{ color: {TEXT_MUTED}; }}
QToolButton#speedButton::menu-indicator {{ image: none; }}

QFrame#statsPanel {{ background: {SURFACE_1}; border: none; border-radius: {RADIUS_LG}; }}

QFrame#settingsCard {{ background: {SURFACE_1}; border: none; border-radius: {RADIUS_MD}; }}
QLabel#fieldCaption {{ color: {TEXT_MUTED}; font-size: {FONT_SMALL}; }}
QLabel#aboutTitle {{ font-size: {FONT_VALUE}; font-weight: {WEIGHT_STRONG}; }}
QLabel#kbd {{
    color: {TEXT_PRIMARY}; background: {SURFACE_2}; border: 1px solid {BORDER};
    border-radius: {RADIUS_SM}; padding: 2px 8px; font-family: {FONT_MONO}; font-size: {FONT_SMALL};
}}
QPushButton#linkDanger {{ background: transparent; color: {ERROR_COLOR}; padding: 4px 0; font-size: {FONT_SMALL}; }}
QPushButton#linkDanger:hover {{ text-decoration: underline; }}
QListWidget#settingsNav::item {{ padding: 8px 12px; margin-bottom: 4px; }}

QFrame#card {{ background: {SURFACE_2}; border: 1px solid {BORDER}; border-radius: {RADIUS_MD}; }}

QFrame#headerSeparator {{ background: {BORDER}; max-width: 1px; min-width: 1px; }}

QLabel#cardTitle {{ color: {TEXT_SECONDARY}; font-size: {FONT_CAPTION}; font-weight: {WEIGHT_STRONG}; letter-spacing: 0.5px; }}
QLabel#cardValue {{ color: {TEXT_PRIMARY}; font-size: {FONT_VALUE}; font-weight: {WEIGHT_STRONG}; }}
QLabel#cardDetail {{ color: {TEXT_SECONDARY}; font-size: {FONT_CAPTION}; }}
QLabel#sectionTitle {{ color: {TEXT_SECONDARY}; font-size: {FONT_CAPTION}; font-weight: {WEIGHT_STRONG}; margin-top: 4px; }}

QProgressBar {{ background: {SURFACE_2}; border: none; border-radius: 4px; }}
QProgressBar::chunk {{ background: {TEXT_SECONDARY}; border-radius: 4px; }}

QListWidget {{
    background: {SURFACE_2}; color: {TEXT_PRIMARY};
    border: none; border-radius: {RADIUS_MD}; font-size: {FONT_SMALL};
}}
QListWidget::item {{ padding: 6px 10px; border-radius: {RADIUS_SM}; }}
QListWidget::item:hover {{ background: {SURFACE_3}; }}
QListWidget::item:selected {{ background: {ACCENT_SOFT}; color: {ACCENT_TEXT}; }}

QListWidget#issues::item {{ margin-right: 6px; }}

QPushButton#combo {{
    background: {SURFACE_2}; color: {TEXT_PRIMARY}; text-align: left;
    border: 1px solid {BORDER_STRONG}; border-radius: {RADIUS_MD}; padding: 7px 28px 7px 10px;
}}
QPushButton#combo:hover, QPushButton#combo:pressed {{ background: {SURFACE_2}; border: 1px solid {TEXT_SECONDARY}; }}
QPushButton#combo:focus {{ border: 1px solid {ACCENT}; }}
QPushButton#combo:disabled {{ color: {TEXT_MUTED}; }}
QPushButton#combo::menu-indicator {{ image: none; }}

QCheckBox {{ color: {TEXT_PRIMARY}; spacing: 8px; font-family: {FONT_FAMILY}; }}
QCheckBox::indicator {{
    width: 17px; height: 17px; border-radius: 5px;
    border: 1px solid {BORDER_STRONG}; background: {SURFACE_2};
}}
QCheckBox::indicator:hover {{ border: 1px solid {ACCENT}; }}
QCheckBox::indicator:focus {{ border: 1px solid {ACCENT}; }}
QCheckBox::indicator:checked {{ background: {ACCENT}; border: 1px solid {ACCENT}; }}


QLineEdit {{
    background: {SURFACE_2}; color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_STRONG}; border-radius: {RADIUS_MD}; padding: 6px 10px;
    selection-background-color: {ACCENT};
}}
QLineEdit:focus {{ border: 1px solid {ACCENT}; }}
QLineEdit:disabled {{ color: {TEXT_MUTED}; }}

QDoubleSpinBox {{
    background: {SURFACE_2}; color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_STRONG}; border-radius: {RADIUS_MD}; padding: 4px 8px;
}}
QDoubleSpinBox:focus {{ border: 1px solid {ACCENT}; }}
QDoubleSpinBox:disabled {{ color: {TEXT_MUTED}; }}
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {{ background: transparent; border: none; width: 18px; }}
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {{ background: {SURFACE_3}; }}

QGroupBox {{
    color: {TEXT_SECONDARY}; font-size: {FONT_CAPTION}; font-weight: {WEIGHT_STRONG};
    border: 1px solid {BORDER}; border-radius: {RADIUS_LG};
    margin-top: 12px; padding-top: 16px;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 6px; color: {TEXT_SECONDARY}; }}

QFrame#issuesPanel {{ background: {SURFACE_1}; border: none; border-radius: {RADIUS_LG}; }}
QLabel#issueSummary {{ color: {TEXT_SECONDARY}; font-size: {FONT_SMALL}; }}
QLabel#issueEmpty {{ color: {SUCCESS}; font-size: {FONT_SMALL}; }}
QLabel#issueDetail {{
    color: {TEXT_SECONDARY}; font-family: {FONT_MONO}; font-size: {FONT_CAPTION};
    background: {SURFACE_2}; border-radius: {RADIUS_SM}; padding: 6px;
}}

QFrame#editorPanel {{ background: {SURFACE_1}; border: none; border-radius: {RADIUS_LG}; }}
QPlainTextEdit#codeEditor {{
    background: {SURFACE_0}; color: {EDITOR_TEXT};
    border: none; border-radius: {RADIUS_MD};
    selection-background-color: {ACCENT};
}}
QLabel#editorStatus {{ color: {WARNING_COLOR}; font-size: {FONT_CAPTION}; font-weight: {WEIGHT_STRONG}; }}
QPushButton#editorToggle:checked {{ background: {ACCENT_SOFT}; color: {ACCENT_TEXT}; }}
QPushButton#saveEdit {{ background: {SURFACE_2}; }}
QPushButton#saveAsEdit {{ background: {SURFACE_2}; }}
QPushButton#editorHelp {{ background: {SURFACE_2}; border-radius: 14px; font-weight: {WEIGHT_STRONG}; }}
QWidget#findBar {{ background: {SURFACE_2}; border-radius: {RADIUS_MD}; }}
QLabel#findStatus {{ color: {WARNING_COLOR}; font-size: {FONT_CAPTION}; }}

QFrame#startPanel {{ background: {SURFACE_0}; }}
QLabel#startTitle {{ color: {TEXT_PRIMARY}; font-size: {FONT_TITLE}; font-weight: {WEIGHT_STRONG}; }}
QLabel#startSubtitle {{ color: {TEXT_SECONDARY}; font-size: {FONT_BODY}; }}
QLabel#startFooter {{ color: {TEXT_MUTED}; font-size: {FONT_CAPTION}; }}

QPushButton#startButton {{
    background: {ACCENT}; padding: 8px 20px; font-size: {FONT_BODY}; font-weight: {WEIGHT_STRONG};
    border-radius: {RADIUS_MD};
}}
QPushButton#startButton:hover {{ background: {ACCENT_HOVER}; }}
QPushButton#startButtonSecondary {{ padding: 8px 20px; font-size: {FONT_BODY}; border-radius: {RADIUS_MD}; }}

QLabel#startHint {{ color: {TEXT_MUTED}; font-size: {FONT_SMALL}; }}
QPushButton#recentRow {{ background: transparent; border: none; border-radius: {RADIUS_SM}; padding: 0; }}
QPushButton#recentRow:hover {{ background: {SURFACE_2}; }}
QLabel#recentName {{ color: {TEXT_PRIMARY}; font-size: {FONT_BODY}; }}
QLabel#recentFolder {{ color: {TEXT_MUTED}; font-size: {FONT_SMALL}; }}
QPushButton#startSettings {{ background: transparent; border: none; border-radius: {RADIUS_MD}; padding: 0; }}
QPushButton#startSettings:hover {{ background: {SURFACE_2}; }}

QScrollBar:vertical {{
    background: transparent; width: 10px; margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_STRONG}; border-radius: 5px; min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: {TEXT_MUTED}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; border: none; background: none; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}

QScrollBar:horizontal {{
    background: transparent; height: 10px; margin: 0;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER_STRONG}; border-radius: 5px; min-width: 24px;
}}
QScrollBar::handle:horizontal:hover {{ background: {TEXT_MUTED}; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; border: none; background: none; }}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{ background: transparent; }}
"""