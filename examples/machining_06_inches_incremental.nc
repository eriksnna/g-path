(EN: Machining example - program in inches with incremental sections)
(PT: Exemplo de usinagem - programa em polegadas com trechos incrementais)
(EN: Dialect: Generic - M3/M4 on, M5 off)
(PT: Dialeto: Generico - M3/M4 liga, M5 desliga)
(EN: Shows G20, inches, and G91, incremental coordinates)
(PT: Demonstra G20, polegadas, e G91, coordenadas incrementais)
(EN: The viewer converts everything to millimeters: 1 in = 25.4 mm)
(PT: O visualizador converte tudo para milimetros: 1 pol = 25.4 mm)

G20 G90
G0 Z0.2
M3 S7000

(EN: oblong slot - two half circles joined by straight lines)
(PT: rasgo oblongo - dois semicirculos ligados por retas)
G0 X1 Y1
G1 Z-0.1 F8
G91                  ; relative moves from here / deslocamentos relativos daqui em diante
G1 X2 F20            ; bottom line, 2 in / reta de baixo, 2 pol
G3 X0 Y1 I0 J0.5     ; right half circle / semicirculo da direita
G1 X-2               ; top line / reta de cima
G3 X0 Y-1 I0 J-0.5   ; left half circle / semicirculo da esquerda
G90                  ; back to absolute / volta para absoluto
G0 Z0.2

(EN: three holes in a row, 1 in apart)
(PT: tres furos em linha, espacados de 1 pol)
G0 X1 Y3
G91
G1 Z-0.5 F5
G0 Z0.5
G0 X1
G1 Z-0.5
G0 Z0.5
G0 X1
G1 Z-0.5
G0 Z0.5
G90

M5
G0 X0 Y0
M2