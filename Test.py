import VNSRK
import sys
import time
from Crypto.Util.Padding import pad, unpad

def build(n):
    z = 2**(n-2)
    inputs = []
    output = VNSRK.Wire(0,0)
    gate = VNSRK.Or(0,0,output)
    output.src = gate
    queue = [gate]
    for i in range(1,2*z):
        gate = queue.pop(0)
        wire1 = VNSRK.Wire(0,gate)
        wire2 = VNSRK.Wire(0,gate)
        gate.in1 = wire1
        gate.in2 = wire2
        gate1 = VNSRK.And(0,0,wire1)
        gate2 = VNSRK.And(0,0,wire2)
        wire1.src = gate1
        wire2.src = gate2
        queue.append(gate1)
        queue.append(gate2)
    for i in range(z):
        gate1 = queue.pop(0)
        gate2 = queue.pop(0)
        wire1 = VNSRK.Wire(0,gate1)
        wire2 = VNSRK.Wire(0,gate1)
        wire3 = VNSRK.Wire(0,gate2)
        wire4 = VNSRK.Wire(0,gate2)
        gate1.in1 = wire1
        gate1.in2 = wire2
        gate2.in1 = wire3
        gate2.in2 = wire4
        gateF1 = VNSRK.Fan(0,wire1,wire4)
        gateF2 = VNSRK.Fan(0,wire2,wire3)
        wire1.src = gateF1
        wire2.src = gateF2
        wire3.src = gateF2
        wire4.src = gateF1
        queue.append(gateF1)
        queue.append(gateF2)
    for i in range(2,2*z):
        gate1 = queue.pop(0)
        gate2 = queue.pop(0)
        wire1 = VNSRK.Wire(0,gate1)
        wire2 = VNSRK.Wire(0,gate2)
        gate1.inFan = wire1
        gate2.inFan = wire2
        gateF = VNSRK.Fan(0,wire1,wire2)
        wire1.src = gateF
        wire2.src = gateF
        queue.append(gateF)
    for i in range(2):
        gate = queue.pop(0)
        wire = VNSRK.Wire(0,gate)
        gate.inFan = wire
        inputs.append(wire)
    return output, inputs

secret = sys.argv[1]
for size in sys.argv[2:]:
    sink, inputs = build(int(size))
    sink.v = pad(str.encode(secret),16)
    start = time.time()
    publish = VNSRK.share(sink)
    result = unpad(str.decode(VNSRK.reconstruct(inputs,publish)),16)
    end = time.time()
    print("Success: {} in time: {}".format(secret==result,end - start))
