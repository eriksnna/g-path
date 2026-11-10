"""Textos da interface em português e inglês. CONTRIBUTING: Pra adicionar um idioma novo,
copie um dos dicionários abaixo e traduza os valores — as CHAVES (lado
esquerdo) nunca mudam, são o que o resto do código usa pra pedir o texto."""
from __future__ import annotations

PT_BR = "pt_BR"
EN = "en"

LANGUAGES = [(PT_BR, "Português (Brasil)"), (EN, "English")]

_STRINGS: dict[str, dict[str, str]] = {
    "app_title": {PT_BR: "G-Path", EN: "G-Path"},

    # --- tela inicial ---------------------------------------------------
    "start_subtitle": {
        PT_BR: "Ferramenta de visualização e simulação 3D de programas G-code.",
        EN: "3D visualization and simulation tool for G-code programs.",
    },
    "start_open_file": {PT_BR: "Abrir arquivo G-code...", EN: "Open G-code file..."},
    "start_blank": {PT_BR: "Começar do zero", EN: "Start from scratch"},

    # --- janela principal: cabeçalho e arquivo ---------------------------
    "file_no_file": {PT_BR: "Nenhum arquivo carregado", EN: "No file loaded"},
    "file_new_unsaved": {PT_BR: "Novo programa (não salvo)", EN: "New program (unsaved)"},
    "editor_toggle": {PT_BR: "Editor", EN: "Editor"},
    "profile_label": {PT_BR: "Perfil: {name}", EN: "Profile: {name}"},

    # --- menus -------------------------------------------------------------
    "menu_file": {PT_BR: "&Arquivo", EN: "&File"},
    "menu_new": {PT_BR: "Novo (em branco)", EN: "New (blank)"},
    "menu_open": {PT_BR: "Abrir G-code...", EN: "Open G-code..."},
    "menu_save": {PT_BR: "Salvar", EN: "Save"},
    "menu_save_as": {PT_BR: "Salvar como...", EN: "Save as..."},
    "menu_close_project": {PT_BR: "Fechar projeto / Redefinir", EN: "Close project / Reset"},
    "menu_quit": {PT_BR: "Sair", EN: "Quit"},
    "menu_edit": {PT_BR: "&Editar", EN: "&Edit"},
    "menu_apply_changes": {PT_BR: "Aplicar alterações", EN: "Apply changes"},
    "menu_toggle_comment": {PT_BR: "Comentar/descomentar linha(s)", EN: "Comment/uncomment line(s)"},
    "menu_find": {PT_BR: "Localizar... (Ctrl+F)", EN: "Find... (Ctrl+F)"},
    "menu_settings": {PT_BR: "&Configurações", EN: "&Settings"},
    "menu_settings_open": {PT_BR: "Ajustes...", EN: "Preferences..."},

    # --- diálogos de arquivo -----------------------------------------------
    "dialog_open_title": {PT_BR: "Abrir G-code", EN: "Open G-code"},
    "dialog_save_title": {PT_BR: "Salvar G-code como", EN: "Save G-code as"},

    # --- status / mensagens ------------------------------------------------
    "status_program_new": {
        PT_BR: "Programa novo. Escreva no editor e aplique (Ctrl+Enter).",
        EN: "New program. Write in the editor and apply (Ctrl+Enter).",
    },
    "status_no_moves": {
        PT_BR: "Nenhum movimento encontrado no arquivo.",
        EN: "No moves found in the file.",
    },
    "status_file_rejected": {PT_BR: "Arquivo recusado: {err}", EN: "File rejected: {err}"},
    "status_open_error": {PT_BR: "Erro ao abrir arquivo: {err}", EN: "Error opening file: {err}"},
    "status_saved_at": {PT_BR: "Salvo em {path}", EN: "Saved to {path}"},
    "status_no_moves_from_line": {
        PT_BR: "Nenhum movimento a partir da linha {line}.",
        EN: "No moves from line {line} onward.",
    },
    "status_line": {
        PT_BR: "movimento {done}/{total}   |   tempo {elapsed} / {total_time}   |   velocidade {speed}x",
        EN: "move {done}/{total}   |   time {elapsed} / {total_time}   |   speed {speed}x",
    },
    "status_active_suffix": {PT_BR: "   |   processo ativo", EN: "   |   process active"},
    "status_issues_suffix": {PT_BR: "   |   {count} problema(s)", EN: "   |   {count} issue(s)"},

    "confirm_discard_title": {PT_BR: "Descartar alterações?", EN: "Discard changes?"},
    "confirm_discard_text": {
        PT_BR: "Há alterações não salvas. Deseja continuar e descartá-las?",
        EN: "There are unsaved changes. Continue and discard them?",
    },
    "save_error_title": {PT_BR: "Erro ao salvar", EN: "Error saving"},
    "save_error_text": {PT_BR: "Não foi possível salvar: {err}", EN: "Could not save: {err}"},
    "unexpected_error_title": {PT_BR: "Erro inesperado", EN: "Unexpected error"},
    "unexpected_error_text": {
        PT_BR: "Ocorreu um erro e a operação não pôde continuar:\n\n{err}",
        EN: "An error occurred and the operation could not continue:\n\n{err}",
    },

    # --- barra de reprodução ------------------------------------------------
    "tooltip_play_pause": {PT_BR: "Reproduzir / pausar", EN: "Play / pause"},
    "tooltip_go_start": {PT_BR: "Ir para o início", EN: "Go to start"},
    "tooltip_rewind": {PT_BR: "Retroceder", EN: "Rewind"},
    "tooltip_forward": {PT_BR: "Avançar", EN: "Forward"},
    "tooltip_go_end": {PT_BR: "Ir para o fim", EN: "Go to end"},
    "label_speed": {PT_BR: "Velocidade", EN: "Speed"},

    # --- painel de estatísticas ----------------------------------------------
    "section_program_summary": {PT_BR: "Resumo do programa", EN: "Program summary"},
    "section_simulation": {PT_BR: "Simulação", EN: "Simulation"},
    "section_mode_prefix": {PT_BR: "Modo: {title}", EN: "Mode: {title}"},
    "card_total_time": {PT_BR: "Tempo total", EN: "Total time"},
    "card_layers": {PT_BR: "Camadas", EN: "Layers"},
    "card_cut_time": {PT_BR: "Tempo de corte", EN: "Cut time"},
    "card_rapid_time": {PT_BR: "Tempo rápido", EN: "Rapid time"},
    "card_cut_length": {PT_BR: "Trajeto de corte", EN: "Cut path"},
    "card_rapid_length": {PT_BR: "Trajeto rápido", EN: "Rapid path"},
    "card_moves": {PT_BR: "Comandos de movimento", EN: "Movement commands"},
    "card_size": {PT_BR: "Dimensões (mm)", EN: "Dimensions (mm)"},
    "card_percent": {PT_BR: "Concluído", EN: "Completed"},
    "card_current": {PT_BR: "Movimento", EN: "Move"},
    "card_elapsed": {PT_BR: "Decorrido", EN: "Elapsed"},
    "card_remaining": {PT_BR: "Restante", EN: "Remaining"},
    "detail_commands": {PT_BR: "{count} comandos", EN: "{count} commands"},
    "detail_breakdown": {PT_BR: "{breakdown}  ·  {segments} segmentos", EN: "{breakdown}  ·  {segments} segments"},
    "detail_none": {PT_BR: "nenhum", EN: "none"},
    "detail_size_axes": {PT_BR: "X × Y × Z", EN: "X × Y × Z"},

    # --- painel de validação -------------------------------------------------
    "validation_title": {PT_BR: "VALIDAÇÃO", EN: "VALIDATION"},
    "validation_hint": {
        PT_BR: "Clique em um problema para ir até a linha.",
        EN: "Click a problem to jump to the line.",
    },
    "validation_empty": {PT_BR: "Nenhum problema encontrado.", EN: "No problems found."},
    "validation_summary": {
        PT_BR: "{errors} erro(s)   ·   {warnings} aviso(s)",
        EN: "{errors} error(s)   ·   {warnings} warning(s)",
    },
    "validation_line_prefix": {PT_BR: "Linha {line}:  {text}", EN: "Line {line}:  {text}"},
    "validation_empty_line": {PT_BR: "(vazia)", EN: "(empty)"},

    # --- editor de G-code ------------------------------------------------------
    "editor_placeholder": {
        PT_BR: "Abra um arquivo G-code para editar aqui.",
        EN: "Open a G-code file to edit here.",
    },
    "editor_search_placeholder": {PT_BR: "Buscar no G-code...", EN: "Search in G-code..."},
    "editor_find_prev": {PT_BR: "< Anterior", EN: "< Previous"},
    "editor_find_next": {PT_BR: "Próximo >", EN: "Next >"},
    "editor_find_close_tip": {PT_BR: "Fechar busca", EN: "Close search"},
    "editor_find_label": {PT_BR: "Buscar:", EN: "Find:"},
    "editor_not_found": {PT_BR: "Não encontrado", EN: "Not found"},
    "editor_apply_button": {PT_BR: "Aplicar (Ctrl+Enter)", EN: "Apply (Ctrl+Enter)"},
    "editor_save_button": {PT_BR: "Salvar", EN: "Save"},
    "editor_save_as_button": {PT_BR: "Salvar como...", EN: "Save as..."},
    "editor_help_tip": {PT_BR: "Atalhos do editor", EN: "Editor shortcuts"},
    "editor_title": {PT_BR: "EDITOR DE G-CODE", EN: "G-CODE EDITOR"},
    "editor_not_applied": {PT_BR: "não aplicado", EN: "not applied"},
    "editor_shortcuts_title": {PT_BR: "Atalhos do editor", EN: "Editor shortcuts"},
    "editor_shortcut_find": {PT_BR: "Buscar texto no editor", EN: "Search text in the editor"},
    "editor_shortcut_apply": {
        PT_BR: "Aplicar as alterações e reinterpretar o programa",
        EN: "Apply changes and reinterpret the program",
    },
    "editor_shortcut_comment": {
        PT_BR: "Comentar ou descomentar a linha atual (ou a seleção)",
        EN: "Comment or uncomment the current line (or selection)",
    },
    "editor_shortcut_save": {PT_BR: "Salvar no arquivo aberto", EN: "Save to the open file"},
    "editor_shortcut_save_as": {
        PT_BR: "Salvar como... (escolher um novo arquivo)",
        EN: "Save as... (choose a new file)",
    },

    # --- controles de modo / camada ----------------------------------------
    "label_mode": {PT_BR: "Modo", EN: "Mode"},
    "label_width": {PT_BR: "Largura", EN: "Width"},
    "label_height": {PT_BR: "Altura", EN: "Height"},
    "label_density": {PT_BR: "Densidade", EN: "Density"},
    "all_layers": {PT_BR: "Todas as camadas", EN: "All layers"},
    "label_layer": {PT_BR: "Camada", EN: "Layer"},
    "checkbox_depth_color": {PT_BR: "Colorir por profundidade", EN: "Color by depth"},

    # --- diálogo de ajustes --------------------------------------------------
    "settings_title": {PT_BR: "Ajustes", EN: "Preferences"},
    "nav_profiles": {PT_BR: "Perfis", EN: "Profiles"},
    "nav_shortcuts": {PT_BR: "Atalhos", EN: "Shortcuts"},
    "nav_appearance": {PT_BR: "Aparência", EN: "Appearance"},
    "profile_combo_label": {PT_BR: "Perfil de máquina:", EN: "Machine profile:"},
    "btn_save_as_profile": {PT_BR: "Salvar como novo perfil...", EN: "Save as new profile..."},
    "btn_remove_profile": {PT_BR: "Remover perfil", EN: "Remove profile"},
    "group_profile_config": {PT_BR: "Configuração do perfil", EN: "Profile configuration"},
    "label_mode_colon": {PT_BR: "Modo:", EN: "Mode:"},
    "label_dialect_colon": {PT_BR: "Dialeto:", EN: "Dialect:"},
    "group_travel_limits": {PT_BR: "Limites de curso (mm)", EN: "Travel limits (mm)"},
    "label_min": {PT_BR: "min", EN: "min"},
    "label_max": {PT_BR: "max", EN: "max"},
    "group_advanced": {PT_BR: "Avançado", EN: "Advanced"},
    "label_rapid_feed": {PT_BR: "Avanço rápido:", EN: "Rapid feed:"},
    "label_default_feed": {PT_BR: "Avanço padrão:", EN: "Default feed:"},
    "label_min_feed": {PT_BR: "Avanço mínimo:", EN: "Minimum feed:"},
    "label_arc_resolution": {PT_BR: "Resolução de arco:", EN: "Arc resolution:"},
    "btn_close": {PT_BR: "Fechar", EN: "Close"},
    "dialog_new_profile_title": {PT_BR: "Salvar como novo perfil", EN: "Save as new profile"},
    "dialog_new_profile_label": {PT_BR: "Nome do perfil:", EN: "Profile name:"},
    "warn_name_used_title": {PT_BR: "Nome em uso", EN: "Name already used"},
    "warn_name_used_text": {
        PT_BR: 'Já existe um perfil chamado "{name}".',
        EN: 'A profile named "{name}" already exists.',
    },
    "info_cant_remove_title": {PT_BR: "Não é possível remover", EN: "Cannot remove"},
    "info_cant_remove_text": {
        PT_BR: "É preciso manter ao menos um perfil.",
        EN: "At least one profile must be kept.",
    },
    "confirm_remove_title": {PT_BR: "Remover perfil", EN: "Remove profile"},
    "confirm_remove_text": {
        PT_BR: 'Remover o perfil "{name}"?',
        EN: 'Remove the profile "{name}"?',
    },
    "shortcuts_label": {PT_BR: "Atalhos do editor:", EN: "Editor shortcuts:"},
    "appearance_language_label": {PT_BR: "Idioma:", EN: "Language:"},
    "appearance_restart_note": {
        PT_BR: "Reinicie o programa para aplicar o novo idioma.",
        EN: "Restart the program to apply the new language.",
    },

    # --- modos de processo (core/modes) ------------------------------------
    "mode_machining_name": {PT_BR: "Usinagem", EN: "Machining"},
    "mode_deposition_name": {PT_BR: "Deposição (WAAM)", EN: "Deposition (WAAM)"},
    "card_avg_feed": {PT_BR: "Avanço médio", EN: "Average feed"},
    "card_avg_feed_detail": {PT_BR: "trajeto de corte ÷ tempo de corte", EN: "cut path ÷ cut time"},
    "card_deposited_material": {PT_BR: "Material depositado", EN: "Deposited material"},
    "card_deposition_rate": {PT_BR: "Taxa de deposição", EN: "Deposition rate"},
    "card_deposited_path": {PT_BR: "Trajeto depositado", EN: "Deposited path"},
    "detail_density": {PT_BR: "densidade", EN: "density"},
    "detail_arc_time": {PT_BR: "em {time} com arco ligado", EN: "in {time} with arc on"},
    "detail_dots_deposited": {PT_BR: "{count} pontos depositados", EN: "{count} dots deposited"},

    # --- dialetos (core/dialect) ---------------------------------------------
    "dialect_generic": {PT_BR: "Genérico (ISO)", EN: "Generic (ISO)"},
    "dialect_arc_m8_m9": {PT_BR: "Arco em M8/M9", EN: "Arc on M8/M9"},
    "dialect_fanuc": {PT_BR: "Fanuc / Haas (P em milissegundos)", EN: "Fanuc / Haas (P in milliseconds)"},
    "dialect_plasma": {PT_BR: "Plasma (tocha em M3/M5)", EN: "Plasma (torch on M3/M5)"},
    "dialect_waam": {PT_BR: "WAAM (arco em M10/M11)", EN: "WAAM (arc on M10/M11)"},

    # --- recursos novos (arquivos recentes, câmera, unidades, tema, formas, comparação) ---
    "menu_open_recent": {PT_BR: "Abrir recente", EN: "Open recent"},
    "menu_recent_empty": {PT_BR: "(nenhum arquivo recente)", EN: "(no recent files)"},
    "menu_export_image": {PT_BR: "Exportar imagem (PNG)...", EN: "Export image (PNG)..."},
    "status_image_saved": {PT_BR: "Imagem salva em {path}", EN: "Image saved to {path}"},
    "menu_compare": {PT_BR: "Comparar com...", EN: "Compare with..."},
    "compare_dialog_title": {PT_BR: "Comparar arquivos", EN: "Compare files"},
    "camera_top": {PT_BR: "Topo", EN: "Top"},
    "camera_front": {PT_BR: "Frente", EN: "Front"},
    "camera_side": {PT_BR: "Lado", EN: "Side"},
    "camera_iso": {PT_BR: "Isométrica", EN: "Isometric"},
    "appearance_unit_label": {PT_BR: "Unidade de exibição:", EN: "Display unit:"},
    "unit_mm": {PT_BR: "Milímetros (mm)", EN: "Millimeters (mm)"},
    "unit_in": {PT_BR: "Polegadas (pol)", EN: "Inches (in)"},
    "appearance_theme_label": {PT_BR: "Tema:", EN: "Theme:"},
    "theme_dark": {PT_BR: "Escuro", EN: "Dark"},
    "theme_light": {PT_BR: "Claro", EN: "Light"},
    "btn_export_profile": {PT_BR: "Exportar perfil...", EN: "Export profile..."},
    "btn_import_profile": {PT_BR: "Importar perfil...", EN: "Import profile..."},
    "dialog_export_profile_title": {PT_BR: "Exportar perfil", EN: "Export profile"},
    "dialog_import_profile_title": {PT_BR: "Importar perfil", EN: "Import profile"},
    "warn_import_invalid_title": {PT_BR: "Arquivo inválido", EN: "Invalid file"},
    "warn_import_invalid_text": {PT_BR: "Não foi possível ler o perfil: {err}", EN: "Could not read profile: {err}"},
    "menu_insert_shape": {PT_BR: "Inserir forma...", EN: "Insert shape..."},
    "shape_dialog_title": {PT_BR: "Inserir forma", EN: "Insert shape"},
    "shape_line": {PT_BR: "Linha", EN: "Line"},
    "shape_rectangle": {PT_BR: "Retângulo", EN: "Rectangle"},
    "shape_circle": {PT_BR: "Círculo", EN: "Circle"},
    "shape_label_radius": {PT_BR: "Raio:", EN: "Radius:"},
    "shape_label_feed": {PT_BR: "Avanço:", EN: "Feed:"},
}

_current = PT_BR


def set_language(code: str) -> None:
    global _current
    if code not in (PT_BR, EN):
        raise ValueError(f"idioma desconhecido: {code}")
    _current = code


def get_language() -> str:
    return _current


def tr(key: str) -> str:
    entry = _STRINGS.get(key)
    if entry is None:
        return key  # chave esquecida — melhor mostrar a chave do que quebrar o app
    return entry.get(_current, entry.get(PT_BR, key))