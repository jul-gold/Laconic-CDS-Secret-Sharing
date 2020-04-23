import VNSRK

def build(circuit)
	stack = [new Wire(0,0)]
	for i in circuit:
		out = stack.pop()
		id = int(i)
		if id == 1:
			in1 = new Wire(0,0)
			in2 = new Wire(0,0)
			gate = new And(in1,in2,out)
			in1.dest = gate
			in2.dest = gate
			stack.append(in2)
			stack.append(in1)
			out.src  =gate
		elif id == 2:
			in1 = new Wire(0,0)
                        in2 = new Wire(0,0)
                        gate = new Or(in1,in2,out)
                        in1.dest = gate
                        in2.dest = gate
                        stack.append(in2)
                        stack.append(in1)
			out.src = gate
		elif id == 0:
			out.src = gate
		elif id % 2 == 1 and id > 2:
			gate = new Fan(0,out,0)
			dict[id+1] = gate
			out.src = gate
		elif id % 2 ==0 and id > 2:
			gate = dict[id]
			in1 = new Wire(0,gate)
			gate.out2 = out
			gate.inFan = in1
			stack.append(in1)
			out.src = gate
			
