from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class And:
    def __init__(self, in1, in2, out):
        self.in1 = in1
        self.in2 = in2
        self.out = out

class Or (And):
    pass

class Fan:
    def __init__(self, inFan, out1, out2):
        self.inFan = inFan
        self.out1 = out1
        self.out2 = out2

class Wire:
    def __init__(self, source, dest):
        self.src = source
        self.dest = dest
        self.v = 0

def enc(key, data):
    cipher = AES.new(key, AES.MODE_CTR)
    ciphertext = cipher.encrypt(data)
    return {"ciphertext" : ciphertext, "nonce" : cipher.nonce}

def dec(key, digest):
    cipher = AES.new(key, AES.MODE_CTR, digest["nonce"])
    data = cipher.decrypt(digest["ciphertext"])

def share(out):
    queue = []
    queue.append(out.src)
    publish = {}
    while len(queue) > 0:
        gate = queue.pop(0)
        if type(gate) is And:
            x = get_random_bytes(16)
            gate.in1.v = x ^ gate.out.v
            queue.append(gate.in1.src)
            gate.in2.v = x
            queue.append(gate.in2.src)
            gate.out.v = 0
        elif type(gate) is Or:
            gate.in1.v = gate.out.v
            queue.append(gate.in1.src)
            gate.in2.v = gate.out.v
            queue.append(gate.in2.src)
            gate.out.v = 0
        elif type(gate) is Fan:
            key = get_random_bytes(16)
            gate.inFan.v = key
            queue.append(gate.inFan.src)
            publish[gate.out1] = enc(key,gate.out1.v)
            publish[gate.out2] = enc(key,gate.out2.v)
            gate.out1.v = 0
            gate.out1.v = 0

def reconstruct(inputs,publish):
    queue = []
    for w in inputs:
            queue.append(w.dest)
    while len(q) > 0:
            gate = queue.pop(0)
            if type(gate) is And:
                    gate.out.v = gate.in1.v ^ gate.in2.v
                    queue.append(gate.out.dest)
            elif type(gate) is Or:
                    gate.out.v = gate.in1.v #something about EVAL ?
                    queue.append(gate.out.dest)
            elif type(gate) is Fan:
                    gate.out1.v = dec(gate.inFan.v,publish[gate.out1])
                    gate.out2.v = dec(gate.inFan.v,publish[gate.out2])
                    queue.append(gate.out1.dest)
                    queue.append(gate.out2.dest)
    return gate.out.v
