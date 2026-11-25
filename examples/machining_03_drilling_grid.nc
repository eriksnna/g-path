(EN: Machining example - 3 x 2 grid of holes with drilling cycles)
(PT: Exemplo de usinagem - grade 3 x 2 de furos com ciclos de furacao)
(EN: Dialect: Generic - M3/M4 on, M5 off)
(PT: Dialeto: Generico - M3/M4 liga, M5 desliga)
(EN: After the first hole of each row, only X changes: the cycle repeats itself)
(PT: Depois do primeiro furo de cada fileira, so o X muda: o ciclo se repete sozinho)

G21 G90
G0 Z5
M3 S6000

(EN: row 1 - G82: drill to Z-6 from R1, dwell 0.5 s at the bottom, return to Z5 - G98)
(PT: fileira 1 - G82: fura ate Z-6 a partir de R1, espera 0.5 s no fundo, volta a Z5 - G98)
G98 G82 X20 Y20 Z-6 R1 P0.5 F100
X50
X80

(EN: row 2 - G83: drill to Z-12 in 4 mm pecks, return only to R1 between holes - G99)
(PT: fileira 2 - G83: fura ate Z-12 em bicadas de 4 mm, volta so ate R1 entre furos - G99)
G99 G83 X20 Y50 Z-12 R1 Q4 F100
X50
X80
G80

G0 Z5
M5
G0 X0 Y0
M2