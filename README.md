# Laconic-CDS-Secret-Sharing

To run:
-Code is compatible with Python3.
-Requires pycrypto library
	-Run "pip install pycrypto" on Mac, or "pip install pycryptodome" on Windows.


First command line argument is the secret, all following represent secrets
"Circuits" are strings of comma-separated numbers that follow the circuit breadth-firs from the sink/output wire. 1s are AND gates, 2s are OR gates, 0s mean reaching an input.


FANOUT gates introduce complication (note that AND/OR would have the same complexity if going from input to output). Because consecutive wires need not line up to consecutive FANOUT gates, we need to record which one is which. To this end, for X>3, n odd X creates a new FANOUT gate & even X+1 sends the wire to the other output of the same FANOUT gate created in X In terms of breadth-first ordering, a fanout gate is considered a dead-end on the first pass (odd number) but searched further once filled (even number).

