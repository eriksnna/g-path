# Changelog

## [0.3.0-beta] - 2026-11-13

### Adicionado
- **NOVA TELA INICIAL**
  - Lista de arquivos recentes
  - Drag-and-Drop de arquivos direto na tela
  - Animação simples
- **REPAGINAÇÃO DA TELA PRINCIPAL**
  - Novo visualizador de leitura digital (DRO)
  - Repaginação na player bar
    - Mudança nos ícones, comportamento, Chips
- **REPAGINAÇÃO NA TELA DE AJUSTES**
  - Design acompanha a página principal
  - Seção "Sobre"
- Sugestão de dialeto automática baseado no código
- Filtro de arquivos
- Novos ícones: [Phosphor Icons](https://phosphoricons.com) — MIT License, © Phosphor Icons
  


### Corrigido
- Bug nas subrotinas: Corrige posicionamento e padronização para não quebrar o g-code
- Bug G92, G28, planos e arcos sem centro e G desconhecido
- Diversos labels hardcoded em português
- Melhor compatibilidade com o parser
- Melhor interpretação de dialetos
- Bug no painel de Issues: Erros de outros arquivos permaneciam após mudar de arquivo ou criar novo projeto
- Bug "no moves found"
- Padronização nos tamanhos (fontes, padding, margin, etc.)
- Avisos agrupados no painel de issues

## [0.2.1-beta] - 2026-11-10

### Corrigido
- Várias labels hardcoded em português

## [0.2.0-beta] - 2026-11-09

### Adicionado
- Funcionalidade "Abrir recente"
- Funcionalidade Arrastar e Soltar
- Botões de vistas de câmeras diferentes
- Suporte ao idioma Italiano

### Corrigido
- Label "Mode" aparecia harcoded em português ("Modo")

## [0.1.0-beta.1] - 2026-11-09
### Adicionado
- Interface bilíngue (português/inglês), com seleção de idioma em Ajustes
- Animações de transição (fade entre telas, hover nos botões, entrada dos stat cards)
- Ícone e logo novos do G-Path
- Primeiro empacotamento em `.exe` via PyInstaller

### Corrigido
- Texto cortado no painel de validação
- Card de comandos de movimento com tradução inconsistente