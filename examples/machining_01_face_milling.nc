(EN: Machining example - face milling in a zigzag)
(PT: Exemplo de usinagem - faceamento em zigue-zague)
(EN: Dialect: Generic - M3/M4 on, M5 off)
(PT: Dialeto: Generico - M3/M4 liga, M5 desliga)
(EN: Removes 1 mm from the top of a 100 x 60 mm block in parallel passes)
(PT: Remove 1 mm do topo de um bloco de 100 x 60 mm em passadas paralelas)

G21 G90
G0 Z5
M3 S8000

G0 X10 Y10
G1 Z-1 F150          ; plunge to cutting depth / desce ate a profundidade de corte

G1 X110 F600         ; pass 1 / passada 1
G1 Y20
G1 X10               ; pass 2 / passada 2
G1 Y30
G1 X110              ; pass 3 / passada 3
G1 Y40
G1 X10               ; pass 4 / passada 4
G1 Y50
G1 X110              ; pass 5 / passada 5
G1 Y60
G1 X10               ; pass 6 / passada 6
G1 Y70
G1 X110              ; pass 7 / passada 7

G0 Z5
M5
G0 X0 Y0
M2