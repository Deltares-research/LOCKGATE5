# Program HYMA1
# Toegevoegde watermassa
# Horizontaal translerende, vertical strip loodrecht op bodem
# aan een zijde water en water erboven

# Laad packages in
import numpy as np
from process import volume, proc

#-----------------------------------------------------------------------------
# Invoer
#-----------------------------------------------------------------------------
s = 6
w = 12
h = 54
uo = 1.
dl = 1.
rl = 1.5
epsn = .025
V = 0.0

#-----------------------------------------------------------------------------
# Rekenen
#-----------------------------------------------------------------------------

# initialiseren
q = np.zeros(s)
p = np.zeros((h+1, w+1))
j = 0

# Bron debieten
for i in range(0, s):
    q[i] = uo * dl

while True:
	Vo = V
	j += 1

	# ------
	# Door het domein
	p = proc(s, h, w, rl, p, q)

	# ------
	# Volume
	V, alfa = volume(s, uo, dl, q, p)
	Vd = V / ((s*dl)**2)
	eps = (V-Vo) / (V/j)
	print(j, V, Vd)

	if eps < epsn:
		for z in range(0, s):
			print(alfa[z])
		break
