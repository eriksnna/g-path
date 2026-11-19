# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e versionamento [SemVer](https://semver.org/lang/pt-BR/).
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [SemVer](https://semver.org/) versioning.

## [0.3.2-beta] - 2026-11-19

### Português

**Adicionado**
- Arcos programados com raio (`R`), além de `I`/`J`
- Arcos nos planos `G18` (XZ) e `G19` (YZ)
- Ciclos de furação `G73`, `G81`, `G82` e `G83`, com `G98`/`G99` e `G80`
- Atalhos `1` a `4` para as vistas de topo, frente, lado e isométrica
- O arquivo aberto é recarregado sozinho quando outro programa o altera; com edições não salvas, o G-Path pergunta antes
- Testes e pacote do Windows gerados automaticamente no GitHub, com o SHA-256 do zip

**Alterado**
- Tocha fica na vertical durante a reprodução no modo deposição
- Deslocamentos em cinza-azulado; o vermelho fica reservado para erros
- Painel lateral: a seção do modo vem logo abaixo do resumo; comandos e dimensões ficam em "Detalhes"
- Campos numéricos só respondem à roda do mouse depois de clicados
- Avanços nos Ajustes com o mesmo número de casas decimais
- README avisa que a simulação não substitui o teste em vazio na máquina

**Corrigido**
- `G04 X` era lido como coordenada: a ferramenta se deslocava em vez de pausar; agora `X` e `U` valem como tempo em segundos
- `G04` sem tempo era ignorado sem aviso
- Checkbox marcado não mostrava o sinal de marcado
- Botão "Editor" continuava aceso com o editor recolhido pela alça

**Segurança**
- Salvar grava primeiro num arquivo temporário: uma falha no meio da gravação não corrompe mais o G-code nem os perfis

### English

**Added**
- Arcs programmed with a radius (`R`), besides `I`/`J`
- Arcs in the `G18` (XZ) and `G19` (YZ) planes
- Drilling cycles `G73`, `G81`, `G82` and `G83`, with `G98`/`G99` and `G80`
- Shortcuts `1` to `4` for the top, front, side and isometric views
- The open file reloads by itself when another program changes it; with unsaved edits, G-Path asks first
- Tests and the Windows package built automatically on GitHub, with the zip's SHA-256

**Changed**
- Torch stays vertical during playback in deposition mode
- Travel moves in gray-blue; red is reserved for errors
- Side panel: the mode section comes right below the summary; commands and dimensions sit under "Details"
- Number fields only react to the mouse wheel after being clicked
- Feed rates in Settings use the same number of decimal places
- README notes that the simulation does not replace a dry run on the machine

**Fixed**
- `G04 X` was read as a coordinate: the tool moved instead of pausing; `X` and `U` now count as time in seconds
- `G04` without a time was silently ignored
- Checked checkbox showed no check mark
- "Editor" button stayed on with the editor collapsed by the handle

**Security**
- Saving writes to a temporary file first: a failure mid-save no longer corrupts the G-code or the profiles

## [0.3.1-beta] - 2026-11-15

### Português

**Adicionado**
- Gizmo de orientação no visualizador: mostra os eixos e alinha a vista com um clique
- Cartão "Cordão" no painel lateral, ao lado dos números que ele altera
- Botão "Reiniciar agora" ao trocar o idioma; o aviso só aparece quando o idioma muda

**Alterado**
- Filtro de camada e "Colorir por profundidade" ficam sobre o visualizador e valem nos dois modos
- Cabeçalho mostra só o nome do arquivo (caminho completo na dica) e ficou menor
- No modo deposição, o resumo fala em tempo e trajeto com arco e sem arco
- Seção "Simulação" removida do painel lateral
- Botões de vista substituídos pelo gizmo
- O pacote para Windows é um .zip: extraia tudo antes de abrir o G-Path.exe

**Corrigido**
- Filtro de camada não escondia nada em programas de deposição por pontos
- Trocar o idioma deixava a tela com textos em duas línguas até reiniciar
- Campos do cordão usavam vírgula decimal, diferente do resto do programa
- Fonte do editor sem alternativa monoespaçada no Linux
- Cartões da mesma linha com valores em alturas diferentes
- Regras de estilo e textos sem uso removidos

### English

**Added**
- Orientation gizmo in the viewer: shows the axes and aligns the view with one click
- "Bead" card in the side panel, next to the figures it changes
- "Restart now" button when changing the language; the note only shows when the language changes

**Changed**
- Layer filter and "Color by depth" sit over the viewer and work in both modes
- Header shows only the file name (full path in the tooltip) and is leaner
- In deposition mode, the summary uses arc-on and arc-off time and path
- "Simulation" section removed from the side panel (the player bar already shows progress)
- View buttons replaced by the gizmo
- The Windows package is a .zip: extract everything before opening G-Path.exe

**Fixed**
- Layer filter hid nothing in dot-deposition programs
- Changing the language left the screen in two languages until restart
- Bead fields used a decimal comma, unlike the rest of the program
- Editor font had no monospace fallback on Linux
- Cards in the same row showed values at different heights
- Unused style rules and strings removed

## [0.3.0-beta] - 2026-11-13

### Português

**Adicionado**
- Tela inicial nova: arquivos recentes, dica de arrastar e soltar, fundo animado e atalho para os Ajustes
- Leitura digital (DRO) no visualizador: posição X/Y/Z, avanço e estado do processo
- Sugestão automática de dialeto quando o arquivo usa códigos de outro dialeto
- Dialeto do perfil visível no cabeçalho
- Atalhos de reprodução: Espaço, setas, Shift + setas (camada), Home e End
- Aba "Sobre" nos Ajustes, com versão, autor e licenças
- 10 arquivos de exemplo (6 de usinagem, 4 de deposição WAAM)
- Pacote de release em .zip, com licenças e exemplos

**Alterado**
- Barra de reprodução em uma linha, com menu de velocidade e passo por movimento
- Tela de Ajustes redesenhada, no mesmo visual da tela principal
- Ícones novos ([Phosphor Icons](https://phosphoricons.com), MIT)
- Problemas repetidos aparecem agrupados no painel de validação
- Tamanhos de fonte, espaçamentos e uso da cor de destaque padronizados

**Corrigido**
- Programas com cabeçalho `O0001` não geravam movimentos
- G92, G28, G30 e G53 eram desenhados como movimento
- Arcos sem centro ou fora do plano XY viravam um círculo incorreto, sem aviso
- Erros do arquivo sumiam quando nenhum movimento era gerado
- Acentos eram perdidos ao salvar arquivos fora de UTF-8
- "Salvar como novo perfil" e "Remover perfil" não funcionavam
- Erro ao abrir arquivo não aparecia na tela inicial
- Ctrl+S só funcionava com o editor visível
- Vários textos fixos em português

**Segurança**
- Limite de movimentos gerados, contra arquivos que esgotam a memória
- Perfis e idioma salvos são validados ao carregar
- Texto de arquivos e caminhos é sempre exibido como texto puro

### English

**Added**
- New start screen: recent files, drag-and-drop hint, animated background and a Settings shortcut
- Digital readout (DRO) in the viewer: X/Y/Z position, feed and process state
- Automatic dialect suggestion when the file uses codes from another dialect
- Profile dialect shown in the header
- Playback shortcuts: Space, arrows, Shift + arrows (layer), Home and End
- "About" tab in Settings, with version, author and licenses
- 10 example files (6 machining, 4 WAAM deposition)
- Release package as a .zip, with licenses and examples

**Changed**
- Single-row playback bar, with a speed menu and stepping by move
- Settings screen redesigned to match the main screen
- New icons ([Phosphor Icons](https://phosphoricons.com), MIT)
- Repeated issues are grouped in the validation panel
- Font sizes, spacing and accent color usage standardized

**Fixed**
- Programs with an `O0001` header produced no moves
- G92, G28, G30 and G53 were drawn as moves
- Arcs without a center or outside the XY plane became a wrong circle, with no warning
- File errors disappeared when no moves were produced
- Accented characters were lost when saving non-UTF-8 files
- "Save as new profile" and "Remove profile" did nothing
- File open errors were not shown on the start screen
- Ctrl+S only worked with the editor visible
- Several labels hardcoded in Portuguese

**Security**
- Cap on generated moves, against files that exhaust memory
- Saved profiles and language are validated on load
- Text from files and paths is always displayed as plain text

## [0.2.1-beta] - 2026-11-10

### Português

**Corrigido**
- Vários textos fixos em português

### English

**Fixed**
- Several labels hardcoded in Portuguese

## [0.2.0-beta] - 2026-11-09

### Português

**Adicionado**
- Abrir arquivos recentes
- Arrastar e soltar arquivos
- Botões de vistas de câmera
- Idioma italiano

**Corrigido**
- Rótulo "Modo" fixo em português

### English

**Added**
- Open recent files
- Drag and drop files
- Camera view buttons
- Italian language

**Fixed**
- "Mode" label hardcoded in Portuguese

## [0.1.0-beta.1] - 2026-11-09

### Português

**Adicionado**
- Interface bilíngue (português e inglês), com seleção de idioma nos Ajustes
- Animações de transição entre telas, nos botões e nos cartões
- Ícone e logo novos
- Primeiro empacotamento em `.exe` com PyInstaller

**Corrigido**
- Texto cortado no painel de validação
- Tradução inconsistente no cartão de comandos de movimento

### English

**Added**
- Bilingual interface (Portuguese and English), with language selection in Settings
- Transition animations between screens, on buttons and on cards
- New icon and logo
- First `.exe` packaging with PyInstaller

**Fixed**
- Clipped text in the validation panel
- Inconsistent translation on the movement commands card