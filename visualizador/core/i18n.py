"""Textos da interface em português, inglês e italiano. Pra adicionar um idioma novo,
copie um dos dicionários abaixo e traduza os valores — as CHAVES (lado esquerdo)
nunca mudam, são o que o resto do código usa pra pedir o texto."""
from __future__ import annotations

PT_BR = "pt_BR"
EN = "en"
IT = "it"

LANGUAGES = [(PT_BR, "Português (Brasil)"), (EN, "English"), (IT, "Italiano")]

_STRINGS: dict[str, dict[str, str]] = {
    "app_title": {PT_BR: "G-Path", EN: "G-Path", IT: "G-Path"},

    # --- tela inicial ---------------------------------------------------
    "start_subtitle": {
        PT_BR: "Ferramenta de visualização e simulação 3D de programas G-code.",
        EN: "3D visualization and simulation tool for G-code programs.",
        IT: "Strumento di visualizzazione e simulazione 3D di programmi G-code.",
    },
    "start_open_file": {PT_BR: "Abrir arquivo G-code...", EN: "Open G-code file...", IT: "Apri file G-code..."},
    "start_drop_hint": {
        PT_BR: "ou arraste um arquivo para esta janela",
        EN: "or drag a file into this window",
        IT: "oppure trascina un file in questa finestra",
    },
    "start_recent_title": {PT_BR: "Recentes", EN: "Recent", IT: "Recenti"},
    "start_blank": {PT_BR: "Começar do zero", EN: "Start from scratch", IT: "Inizia da zero"},

    # --- janela principal: cabeçalho e arquivo ---------------------------
    "file_no_file": {PT_BR: "Nenhum arquivo carregado", EN: "No file loaded", IT: "Nessun file caricato"},
    "file_new_unsaved": {PT_BR: "Novo programa (não salvo)", EN: "New program (unsaved)", IT: "Nuovo programma (non salvato)"},
    "editor_toggle": {PT_BR: "Editor", EN: "Editor", IT: "Editor"},
    "profile_label": {PT_BR: "Perfil: {name}", EN: "Profile: {name}", IT: "Profilo: {name}"},

    # --- menus -------------------------------------------------------------
    "menu_file": {PT_BR: "&Arquivo", EN: "&File", IT: "&File"},
    "menu_new": {PT_BR: "Novo (em branco)", EN: "New (blank)", IT: "Nuovo (vuoto)"},
    "menu_open": {PT_BR: "Abrir G-code...", EN: "Open G-code...", IT: "Apri G-code..."},
    "menu_open_recent": {PT_BR: "Abrir recente", EN: "Open recent", IT: "Apri recente"},
    "menu_recent_empty": {PT_BR: "(nenhum arquivo recente)", EN: "(no recent files)", IT: "(nessun file recente)"},
    "menu_save": {PT_BR: "Salvar", EN: "Save", IT: "Salva"},
    "menu_save_as": {PT_BR: "Salvar como...", EN: "Save as...", IT: "Salva come..."},
    "menu_close_project": {PT_BR: "Fechar projeto / Redefinir", EN: "Close project / Reset", IT: "Chiudi progetto / Ripristina"},
    "menu_quit": {PT_BR: "Sair", EN: "Quit", IT: "Esci"},
    "menu_edit": {PT_BR: "&Editar", EN: "&Edit", IT: "&Modifica"},
    "menu_apply_changes": {PT_BR: "Aplicar alterações", EN: "Apply changes", IT: "Applica modifiche"},
    "menu_toggle_comment": {PT_BR: "Comentar/descomentar linha(s)", EN: "Comment/uncomment line(s)", IT: "Commenta/scommenta riga(he)"},
    "menu_find": {PT_BR: "Localizar... (Ctrl+F)", EN: "Find... (Ctrl+F)", IT: "Trova... (Ctrl+F)"},
    "menu_settings": {PT_BR: "&Configurações", EN: "&Settings", IT: "&Impostazioni"},
    "menu_settings_open": {PT_BR: "Ajustes...", EN: "Preferences...", IT: "Preferenze..."},

    # --- diálogos de arquivo -----------------------------------------------
    "dialog_open_title": {PT_BR: "Abrir G-code", EN: "Open G-code", IT: "Apri G-code"},
    "dialog_save_title": {PT_BR: "Salvar G-code como", EN: "Save G-code as", IT: "Salva G-code come"},

    # --- status / mensagens ------------------------------------------------
    "status_program_new": {
        PT_BR: "Programa novo. Escreva no editor e aplique (Ctrl+Enter).",
        EN: "New program. Write in the editor and apply (Ctrl+Enter).",
        IT: "Nuovo programma. Scrivi nell'editor e applica (Ctrl+Invio).",
    },
    "status_no_moves": {
        PT_BR: "Nenhum movimento encontrado no arquivo.",
        EN: "No moves found in the file.",
        IT: "Nessun movimento trovato nel file.",
    },
    "status_no_moves_see_issues": {
        PT_BR: "Nenhum movimento gerado: veja os {count} problema(s) no painel de validação",
        EN: "No moves generated: see the {count} issue(s) in the validation panel",
        IT: "Nessun movimento generato: vedi i {count} problemi nel pannello di convalida",
    },
    "open_error_title": {PT_BR: "Não foi possível abrir", EN: "Could not open", IT: "Impossibile aprire"},
    "file_filter_all": {PT_BR: "Todos os arquivos", EN: "All files", IT: "Tutti i file"},
    "file_too_large": {
        PT_BR: "arquivo tem {size} MB, acima do limite de {limit} MB",
        EN: "file is {size} MB, above the {limit} MB limit",
        IT: "il file è di {size} MB, oltre il limite di {limit} MB",
    },
    "file_line_too_long": {
        PT_BR: "linha {line} tem {length} caracteres, acima do limite de {limit}; o arquivo pode estar corrompido",
        EN: "line {line} has {length} characters, above the {limit} limit; the file may be corrupted",
        IT: "la riga {line} ha {length} caratteri, oltre il limite di {limit}; il file potrebbe essere danneggiato",
    },
    "status_file_rejected": {PT_BR: "Arquivo recusado: {err}", EN: "File rejected: {err}", IT: "File rifiutato: {err}"},
    "status_open_error": {PT_BR: "Erro ao abrir arquivo: {err}", EN: "Error opening file: {err}", IT: "Errore nell'apertura del file: {err}"},
    "status_saved_at": {PT_BR: "Salvo em {path}", EN: "Saved to {path}", IT: "Salvato in {path}"},
    "status_no_moves_from_line": {
        PT_BR: "Nenhum movimento a partir da linha {line}.",
        EN: "No moves from line {line} onward.",
        IT: "Nessun movimento a partire dalla riga {line}.",
    },
    "confirm_discard_title": {PT_BR: "Descartar alterações?", EN: "Discard changes?", IT: "Scartare le modifiche?"},
    "confirm_discard_text": {
        PT_BR: "Há alterações não salvas. Deseja continuar e descartá-las?",
        EN: "There are unsaved changes. Continue and discard them?",
        IT: "Ci sono modifiche non salvate. Continuare e scartarle?",
    },
    "save_error_title": {PT_BR: "Erro ao salvar", EN: "Error saving", IT: "Errore nel salvataggio"},
    "save_error_text": {PT_BR: "Não foi possível salvar: {err}", EN: "Could not save: {err}", IT: "Impossibile salvare: {err}"},
    "unexpected_error_title": {PT_BR: "Erro inesperado", EN: "Unexpected error", IT: "Errore imprevisto"},
    "unexpected_error_text": {
        PT_BR: "Ocorreu um erro e a operação não pôde continuar:\n\n{err}",
        EN: "An error occurred and the operation could not continue:\n\n{err}",
        IT: "Si è verificato un errore e l'operazione non può continuare:\n\n{err}",
    },

    # --- barra de reprodução ------------------------------------------------
    "tooltip_play_pause": {PT_BR: "Reproduzir / pausar", EN: "Play / pause", IT: "Riproduci / pausa"},
    "tooltip_go_start": {PT_BR: "Ir para o início", EN: "Go to start", IT: "Vai all'inizio"},
    "tooltip_rewind": {PT_BR: "Retroceder", EN: "Rewind", IT: "Indietro"},
    "tooltip_forward": {PT_BR: "Avançar", EN: "Forward", IT: "Avanti"},
    "tooltip_go_end": {PT_BR: "Ir para o fim", EN: "Go to end", IT: "Vai alla fine"},
    "tooltip_step_back": {
        PT_BR: "Movimento anterior (Shift: camada anterior)",
        EN: "Previous move (Shift: previous layer)",
        IT: "Movimento precedente (Shift: strato precedente)",
    },
    "tooltip_step_forward": {
        PT_BR: "Próximo movimento (Shift: próxima camada)",
        EN: "Next move (Shift: next layer)",
        IT: "Movimento successivo (Shift: strato successivo)",
    },
    "player_layer_chip": {PT_BR: "Camada {layer}/{total}", EN: "Layer {layer}/{total}", IT: "Strato {layer}/{total}"},
        "profile_dialect_tooltip": {
        PT_BR: "Dialeto do perfil: o processo liga e desliga em {codes}",
        EN: "Profile dialect: the process turns on and off with {codes}",
        IT: "Dialetto del profilo: il processo si attiva e disattiva con {codes}",
    },
    "dialect_suggestion": {
        PT_BR: "Este programa usa {codes} para ligar e desligar o processo, mas o dialeto atual é {current}.",
        EN: "This program uses {codes} to turn the process on and off, but the current dialect is {current}.",
        IT: "Questo programma usa {codes} per attivare e disattivare il processo, ma il dialetto attuale è {current}.",
    },
    "dialect_suggestion_action": {PT_BR: "Usar {name}", EN: "Use {name}", IT: "Usa {name}"},
        "validation_repeated": {
        PT_BR: "Ocorre {count} vezes (a linha é executada mais de uma vez)",
        EN: "Occurs {count} times (the line runs more than once)",
        IT: "Si verifica {count} volte (la riga viene eseguita più volte)",
    },
    "dro_process_on": {PT_BR: "ligado", EN: "on", IT: "attivo"},
    "dro_process_off": {PT_BR: "desligado", EN: "off", IT: "spento"},
    "label_speed": {PT_BR: "Velocidade", EN: "Speed", IT: "Velocità"},
    "chip_process_on": {PT_BR: "Processo ligado", EN: "Process on", IT: "Processo attivo"},
    "chip_process_off": {PT_BR: "Processo desligado", EN: "Process off", IT: "Processo spento"},

    # --- painel de estatísticas ----------------------------------------------
    "section_program_summary": {PT_BR: "Resumo do programa", EN: "Program summary", IT: "Riepilogo del programma"},
    "section_simulation": {PT_BR: "Simulação", EN: "Simulation", IT: "Simulazione"},
    "section_mode_prefix": {PT_BR: "Modo: {title}", EN: "Mode: {title}", IT: "Modalità: {title}"},
    "card_total_time": {PT_BR: "Tempo total", EN: "Total time", IT: "Tempo totale"},
    "card_layers": {PT_BR: "Camadas", EN: "Layers", IT: "Strati"},
    "card_cut_time": {PT_BR: "Tempo de corte", EN: "Cut time", IT: "Tempo di taglio"},
    "card_rapid_time": {PT_BR: "Tempo rápido", EN: "Rapid time", IT: "Tempo rapido"},
    "card_cut_length": {PT_BR: "Trajeto de corte", EN: "Cut path", IT: "Percorso di taglio"},
    "card_rapid_length": {PT_BR: "Trajeto rápido", EN: "Rapid path", IT: "Percorso rapido"},
    "card_moves": {PT_BR: "Comandos de movimento", EN: "Movement commands", IT: "Comandi di movimento"},
    "card_size": {PT_BR: "Dimensões (mm)", EN: "Dimensions (mm)", IT: "Dimensioni (mm)"},
    "card_percent": {PT_BR: "Concluído", EN: "Completed", IT: "Completato"},
    "card_current": {PT_BR: "Movimento", EN: "Move", IT: "Movimento"},
    "card_elapsed": {PT_BR: "Decorrido", EN: "Elapsed", IT: "Trascorso"},
    "card_remaining": {PT_BR: "Restante", EN: "Remaining", IT: "Rimanente"},
    "detail_commands": {PT_BR: "{count} comandos", EN: "{count} commands", IT: "{count} comandi"},
    "detail_breakdown": {PT_BR: "{breakdown}  ·  {segments} segmentos", EN: "{breakdown}  ·  {segments} segments", IT: "{breakdown}  ·  {segments} segmenti"},
    "detail_none": {PT_BR: "nenhum", EN: "none", IT: "nessuno"},
    "detail_size_axes": {PT_BR: "X × Y × Z", EN: "X × Y × Z", IT: "X × Y × Z"},

    # --- painel de validação -------------------------------------------------
    "validation_title": {PT_BR: "VALIDAÇÃO", EN: "VALIDATION", IT: "VALIDAZIONE"},
    "validation_hint": {
        PT_BR: "Clique em um problema para ir até a linha.",
        EN: "Click a problem to jump to the line.",
        IT: "Fai clic su un problema per andare alla riga.",
    },
    "validation_empty": {PT_BR: "Nenhum problema encontrado.", EN: "No problems found.", IT: "Nessun problema trovato."},
    "validation_summary": {
        PT_BR: "{errors} erro(s)   ·   {warnings} aviso(s)",
        EN: "{errors} error(s)   ·   {warnings} warning(s)",
        IT: "{errors} errore/i   ·   {warnings} avviso/i",
    },
    "validation_line_prefix": {PT_BR: "Linha {line}:  {text}", EN: "Line {line}:  {text}", IT: "Riga {line}:  {text}"},
    "validation_empty_line": {PT_BR: "(vazia)", EN: "(empty)", IT: "(vuota)"},

    # --- editor de G-code ------------------------------------------------------
    "editor_placeholder": {
        PT_BR: "Abra um arquivo G-code para editar aqui.",
        EN: "Open a G-code file to edit here.",
        IT: "Apri un file G-code per modificarlo qui.",
    },
    "editor_search_placeholder": {PT_BR: "Buscar no G-code...", EN: "Search in G-code...", IT: "Cerca nel G-code..."},
    "editor_find_prev": {PT_BR: "< Anterior", EN: "< Previous", IT: "< Precedente"},
    "editor_find_next": {PT_BR: "Próximo >", EN: "Next >", IT: "Successivo >"},
    "editor_find_close_tip": {PT_BR: "Fechar busca", EN: "Close search", IT: "Chiudi ricerca"},
    "editor_find_label": {PT_BR: "Buscar:", EN: "Find:", IT: "Cerca:"},
    "editor_not_found": {PT_BR: "Não encontrado", EN: "Not found", IT: "Non trovato"},
    "editor_apply_button": {PT_BR: "Aplicar (Ctrl+Enter)", EN: "Apply (Ctrl+Enter)", IT: "Applica (Ctrl+Invio)"},
    "editor_save_button": {PT_BR: "Salvar", EN: "Save", IT: "Salva"},
    "editor_save_as_button": {PT_BR: "Salvar como...", EN: "Save as...", IT: "Salva come..."},
    "editor_help_tip": {PT_BR: "Atalhos do editor", EN: "Editor shortcuts", IT: "Scorciatoie dell'editor"},
    "editor_title": {PT_BR: "EDITOR DE G-CODE", EN: "G-CODE EDITOR", IT: "EDITOR G-CODE"},
    "editor_not_applied": {PT_BR: "não aplicado", EN: "not applied", IT: "non applicato"},
    "editor_shortcuts_title": {PT_BR: "Atalhos do editor", EN: "Editor shortcuts", IT: "Scorciatoie dell'editor"},
    "editor_shortcut_find": {PT_BR: "Buscar texto no editor", EN: "Search text in the editor", IT: "Cerca testo nell'editor"},
    "editor_shortcut_apply": {
        PT_BR: "Aplicar as alterações e reinterpretar o programa",
        EN: "Apply changes and reinterpret the program",
        IT: "Applica le modifiche e reinterpreta il programma",
    },
    "editor_shortcut_comment": {
        PT_BR: "Comentar ou descomentar a linha atual (ou a seleção)",
        EN: "Comment or uncomment the current line (or selection)",
        IT: "Commenta o scommenta la riga corrente (o la selezione)",
    },
    "editor_shortcut_save": {PT_BR: "Salvar no arquivo aberto", EN: "Save to the open file", IT: "Salva nel file aperto"},
    "editor_shortcut_save_as": {
        PT_BR: "Salvar como... (escolher um novo arquivo)",
        EN: "Save as... (choose a new file)",
        IT: "Salva come... (scegli un nuovo file)",
    },

    # --- controles de modo / camada ----------------------------------------
    "label_mode": {PT_BR: "Modo", EN: "Mode", IT: "Modalità"},
    "label_width": {PT_BR: "Largura", EN: "Width", IT: "Larghezza"},
    "label_height": {PT_BR: "Altura", EN: "Height", IT: "Altezza"},
    "label_density": {PT_BR: "Densidade", EN: "Density", IT: "Densità"},
    "all_layers": {PT_BR: "Todas as camadas", EN: "All layers", IT: "Tutti gli strati"},
    "label_layer": {PT_BR: "Camada", EN: "Layer", IT: "Strato"},
    "checkbox_depth_color": {PT_BR: "Colorir por profundidade", EN: "Color by depth", IT: "Colora per profondità"},

    # --- diálogo de ajustes --------------------------------------------------
    "settings_title": {PT_BR: "Ajustes", EN: "Preferences", IT: "Preferenze"},
    "nav_profiles": {PT_BR: "Perfis", EN: "Profiles", IT: "Profili"},
    "nav_shortcuts": {PT_BR: "Atalhos", EN: "Shortcuts", IT: "Scorciatoie"},
    "nav_appearance": {PT_BR: "Aparência", EN: "Appearance", IT: "Aspetto"},
    "profile_combo_label": {PT_BR: "Perfil de máquina:", EN: "Machine profile:", IT: "Profilo macchina:"},
    "btn_save_as_profile": {PT_BR: "Salvar como novo perfil...", EN: "Save as new profile...", IT: "Salva come nuovo profilo..."},
    "btn_remove_profile": {PT_BR: "Remover perfil", EN: "Remove profile", IT: "Rimuovi profilo"},
    "group_profile_config": {PT_BR: "Configuração do perfil", EN: "Profile configuration", IT: "Configurazione del profilo"},
    "label_mode_colon": {PT_BR: "Modo:", EN: "Mode:", IT: "Modalità:"},
    "label_dialect_colon": {PT_BR: "Dialeto:", EN: "Dialect:", IT: "Dialetto:"},
    "group_travel_limits": {PT_BR: "Limites de curso (mm)", EN: "Travel limits (mm)", IT: "Limiti di corsa (mm)"},
    "label_min": {PT_BR: "min", EN: "min", IT: "min"},
    "label_max": {PT_BR: "max", EN: "max", IT: "max"},
    "group_advanced": {PT_BR: "Avançado", EN: "Advanced", IT: "Avanzate"},
    "label_rapid_feed": {PT_BR: "Avanço rápido:", EN: "Rapid feed:", IT: "Avanzamento rapido:"},
    "label_default_feed": {PT_BR: "Avanço padrão:", EN: "Default feed:", IT: "Avanzamento predefinito:"},
    "label_min_feed": {PT_BR: "Avanço mínimo:", EN: "Minimum feed:", IT: "Avanzamento minimo:"},
    "label_arc_resolution": {PT_BR: "Resolução de arco:", EN: "Arc resolution:", IT: "Risoluzione dell'arco:"},
    "btn_close": {PT_BR: "Fechar", EN: "Close", IT: "Chiudi"},
    "dialog_new_profile_title": {PT_BR: "Salvar como novo perfil", EN: "Save as new profile", IT: "Salva come nuovo profilo"},
    "dialog_new_profile_label": {PT_BR: "Nome do perfil:", EN: "Profile name:", IT: "Nome del profilo:"},
    "warn_name_used_title": {PT_BR: "Nome em uso", EN: "Name already used", IT: "Nome già in uso"},
    "warn_name_used_text": {
        PT_BR: 'Já existe um perfil chamado "{name}".',
        EN: 'A profile named "{name}" already exists.',
        IT: 'Esiste già un profilo chiamato "{name}".',
    },
    "info_cant_remove_title": {PT_BR: "Não é possível remover", EN: "Cannot remove", IT: "Impossibile rimuovere"},
    "info_cant_remove_text": {
        PT_BR: "É preciso manter ao menos um perfil.",
        EN: "At least one profile must be kept.",
        IT: "È necessario mantenere almeno un profilo.",
    },
    "confirm_remove_title": {PT_BR: "Remover perfil", EN: "Remove profile", IT: "Rimuovi profilo"},
    "confirm_remove_text": {
        PT_BR: 'Remover o perfil "{name}"?',
        EN: 'Remove the profile "{name}"?',
        IT: 'Rimuovere il profilo "{name}"?',
    },
    "shortcuts_label": {PT_BR: "Atalhos do editor:", EN: "Editor shortcuts:", IT: "Scorciatoie dell'editor:"},
    "appearance_language_label": {PT_BR: "Idioma:", EN: "Language:", IT: "Lingua:"},
    "appearance_restart_note": {
        PT_BR: "Reinicie o programa para aplicar o novo idioma.",
        EN: "Restart the program to apply the new language.",
        IT: "Riavvia il programma per applicare la nuova lingua.",
    },

    # --- modos de processo (core/modes) ------------------------------------
    "mode_machining_name": {PT_BR: "Usinagem", EN: "Machining", IT: "Lavorazione"},
    "mode_deposition_name": {PT_BR: "Deposição (WAAM)", EN: "Deposition (WAAM)", IT: "Deposizione (WAAM)"},
    "card_avg_feed": {PT_BR: "Avanço médio", EN: "Average feed", IT: "Avanzamento medio"},
    "card_avg_feed_detail": {PT_BR: "trajeto de corte ÷ tempo de corte", EN: "cut path ÷ cut time", IT: "percorso di taglio ÷ tempo di taglio"},
    "card_deposited_material": {PT_BR: "Material depositado", EN: "Deposited material", IT: "Materiale depositato"},
    "card_deposition_rate": {PT_BR: "Taxa de deposição", EN: "Deposition rate", IT: "Tasso di deposizione"},
    "card_deposited_path": {PT_BR: "Trajeto depositado", EN: "Deposited path", IT: "Percorso depositato"},
    "detail_density": {PT_BR: "densidade", EN: "density", IT: "densità"},
    "detail_arc_time": {PT_BR: "em {time} com arco ligado", EN: "in {time} with arc on", IT: "in {time} con arco acceso"},
    "detail_dots_deposited": {PT_BR: "{count} pontos depositados", EN: "{count} dots deposited", IT: "{count} punti depositati"},

    # --- dialetos (core/dialect) ---------------------------------------------
    "dialect_generic": {PT_BR: "Genérico (ISO)", EN: "Generic (ISO)", IT: "Generico (ISO)"},
    "dialect_arc_m8_m9": {PT_BR: "Arco em M8/M9", EN: "Arc on M8/M9", IT: "Arco su M8/M9"},
    "dialect_fanuc": {PT_BR: "Fanuc / Haas (P em milissegundos)", EN: "Fanuc / Haas (P in milliseconds)", IT: "Fanuc / Haas (P in millisecondi)"},
    "dialect_plasma": {PT_BR: "Plasma (tocha em M3/M5)", EN: "Plasma (torch on M3/M5)", IT: "Plasma (torcia su M3/M5)"},
    "dialect_waam": {PT_BR: "WAAM (arco em M10/M11)", EN: "WAAM (arc on M10/M11)", IT: "WAAM (arco su M10/M11)"},

    # --- mensagens de validação (parser/expander/modos) ----------------------
    "severity_error": {PT_BR: "Erro", EN: "Error", IT: "Errore"},
    "severity_warning": {PT_BR: "Aviso", EN: "Warning", IT: "Avviso"},

    "issue_g_not_simulated": {
        PT_BR: "G{code} não é simulado; coordenadas da linha ignoradas",
        EN: "G{code} is not simulated; coordinates on this line ignored",
        IT: "G{code} non è simulato; coordinate della riga ignorate",
    },
    "issue_g_unknown": {
        PT_BR: "G{code} não reconhecido; ignorado",
        EN: "G{code} not recognized; ignored",
        IT: "G{code} non riconosciuto; ignorato",
    },
    "issue_arc_plane_unsupported": {
        PT_BR: "arco no plano G{plane} não suportado; só G17 (XY)",
        EN: "arc in plane G{plane} is not supported; only G17 (XY)",
        IT: "arco nel piano G{plane} non supportato; solo G17 (XY)",
    },
    "issue_arc_missing_center": {
        PT_BR: "arco sem centro: informe I e/ou J",
        EN: "arc without center: provide I and/or J",
        IT: "arco senza centro: indica I e/o J",
    },

    "issue_arc_r_unsupported": {
        PT_BR: "arco com R não suportado; use I/J",
        EN: "arc with R is not supported; use I/J",
        IT: "arco con R non supportato; usa I/J",
    },
    "issue_feed_missing": {
        PT_BR: "avanço F ausente; usando {feed} mm/min",
        EN: "missing feed F; using {feed} mm/min",
        IT: "avanzamento F assente; uso {feed} mm/min",
    },
    "issue_out_of_bounds": {
        PT_BR: "fora da área de trabalho: {axis} = {value} (faixa {low} a {high} mm)",
        EN: "outside the work area: {axis} = {value} (range {low} to {high} mm)",
        IT: "fuori dall'area di lavoro: {axis} = {value} (intervallo {low} - {high} mm)",
    },
    "issue_sub_redefined": {
        PT_BR: "sub-rotina O{number} definida mais de uma vez",
        EN: "subroutine O{number} defined more than once",
        IT: "sottoprogramma O{number} definito più di una volta",
    },
    "issue_control_code_alone": {
        PT_BR: "M98, M99 e M30 devem estar sozinhos na linha; linha ignorada",
        EN: "M98, M99 and M30 must be alone on the line; line ignored",
        IT: "M98, M99 e M30 devono essere da soli sulla riga; riga ignorata",
    },
    "issue_call_missing_p": {
        PT_BR: "M98 sem P (número da sub-rotina)",
        EN: "M98 without P (subroutine number)",
        IT: "M98 senza P (numero del sottoprogramma)",
    },
    "issue_call_invalid_l": {
        PT_BR: "L inválido no M98: {value}",
        EN: "invalid L in M98: {value}",
        IT: "L non valido in M98: {value}",
    },
    "issue_sub_not_found": {
        PT_BR: "sub-rotina O{number} não encontrada",
        EN: "subroutine O{number} not found",
        IT: "sottoprogramma O{number} non trovato",
    },
    "issue_call_too_deep": {
        PT_BR: "chamadas aninhadas acima de {max_depth} níveis; possível recursão",
        EN: "nested calls beyond {max_depth} levels; possible recursion",
        IT: "chiamate annidate oltre {max_depth} livelli; possibile ricorsione",
    },
    "issue_expansion_too_long": {
        PT_BR: "programa expandido acima de {max_lines} linhas; expansão interrompida",
        EN: "expanded program beyond {max_lines} lines; expansion stopped",
        IT: "programma espanso oltre {max_lines} righe; espansione interrotta",
    },
    "issue_expr_invalid": {
        PT_BR: "expressão inválida: {expr}",
        EN: "invalid expression: {expr}",
        IT: "espressione non valida: {expr}",
    },
    "issue_division_by_zero": {
        PT_BR: "divisão por zero em {expr}",
        EN: "division by zero in {expr}",
        IT: "divisione per zero in {expr}",
    },
    "issue_expr_unsupported": {
        PT_BR: "expressão não suportada: {expr}",
        EN: "unsupported expression: {expr}",
        IT: "espressione non supportata: {expr}",
    },
    "issue_variable_undefined": {
        PT_BR: "variável #{number} não definida",
        EN: "variable #{number} not defined",
        IT: "variabile #{number} non definita",
    },
    "issue_machining_no_process": {
        PT_BR: "corte sem processo ligado (M3/M8 não ativado no dialeto?)",
        EN: "cut with no process on (M3/M8 not enabled in the dialect?)",
        IT: "taglio senza processo attivo (M3/M8 non attivato nel dialetto?)",
    },
    "issue_deposition_no_deposit": {
        PT_BR: "nenhum depósito encontrado: nenhum movimento com processo ligado. "
               "Verifique o dialeto (códigos de liga/desliga do arco)",
        EN: "no deposition found: no move with the process on. "
            "Check the dialect (arc on/off codes)",
        IT: "nessuna deposizione trovata: nessun movimento con processo attivo. "
            "Controlla il dialetto (codici di accensione/spegnimento dell'arco)",
    },
    "issue_deposition_rapid_on": {
        PT_BR: "deslocamento rápido (G0) com processo ligado",
        EN: "rapid move (G0) with the process on",
        IT: "movimento rapido (G0) con processo attivo",
    },
    "issue_deposition_layer_height": {
        PT_BR: "passo entre camadas de {step} mm; cordão configurado com {height} mm",
        EN: "layer step of {step} mm; bead configured at {height} mm",
        IT: "passo tra gli strati di {step} mm; cordone configurato a {height} mm",
    },

    # --- vistas de câmera (se você já aplicou o item 3 do passo anterior) ----
    "camera_top": {PT_BR: "Topo", EN: "Top", IT: "Alto"},
    "camera_front": {PT_BR: "Frente", EN: "Front", IT: "Fronte"},
    "camera_side": {PT_BR: "Lado", EN: "Side", IT: "Lato"},
    "camera_iso": {PT_BR: "Isométrica", EN: "Isometric", IT: "Isometrica"},

    "profile_default_name": {PT_BR: "Minha máquina", EN: "My machine", IT: "La mia macchina"},
    "profile_unlimited_name": {
        PT_BR: "Sem limite (ignorar área de trabalho)",
        EN: "No limit (ignore work area)",
        IT: "Nessun limite (ignora l'area di lavoro)",
    },
}

_current = PT_BR


def set_language(code: str) -> None:
    global _current
    if code not in (PT_BR, EN, IT):
        raise ValueError(f"idioma desconhecido: {code}")
    _current = code


def get_language() -> str:
    return _current


def tr(key: str) -> str:
    entry = _STRINGS.get(key)
    if entry is None:
        return key  # chave esquecida — melhor mostrar a chave do que quebrar o app
    return entry.get(_current, entry.get(PT_BR, key))