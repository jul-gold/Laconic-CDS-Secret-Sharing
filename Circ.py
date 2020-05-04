import sys
import VNSRK
import time
from Crypto.Util.Padding import pad, unpad

def build(circuit):
    secret = VNSRK.Wire(0,0)
    inputs = []
    stack = [secret]
    fans = {}
    circ = circuit.split(",")
    for i in circ:
        out = stack.pop()
        id = int(i)
        if id == 1:
            in1 = VNSRK.Wire(0,0)
            in2 = VNSRK.Wire(0,0)
            gate = VNSRK.And(in1,in2,out)
            in1.dest = gate
            in2.dest = gate
            stack.append(in2)
            stack.append(in1)
            out.src = gate
        elif id == 2:
            in1 = VNSRK.Wire(0,0)
            in2 = VNSRK.Wire(0,0)
            gate = VNSRK.Or(in1,in2,out)
            in1.dest = gate
            in2.dest = gate
            stack.append(in2)
            stack.append(in1)
            out.src = gate
        elif id == 0:
            inputs.append(out)
        elif (id % 2 == 1) and (id > 2):
            gate = VNSRK.Fan(0,out,0)
            fans[id+1] = gate
            out.src = gate
        elif (id % 2 == 0) and (id > 2):
            gate = fans[id]
            in1 = VNSRK.Wire(0,gate)
            gate.out2 = out
            gate.inFan = in1
            stack.append(in1)
            out.src = gate
    return secret, inputs

secret = sys.argv[1]
for circuit in sys.argv[2:]:
    sink, inputs = build(circuit)
    sink.v = pad(str.encode(secret),16)
    start = time.time()
    publish = VNSRK.share(sink)
    result = unpad(str.decode(VNSRK.reconstruct(inputs,publish)),16)
    end = time.time()
    print("Success: {} in time: {}".format(secret==result,end - start))
