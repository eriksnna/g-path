# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e versionamento [SemVer](https://semver.org/lang/pt-BR/).
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [SemVer](https://semver.org/) versioning.

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