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
		elif id == 2:
			in1 = new Wire(0,0)
                        in2 = new Wire(0,0)
                        gate = new Or(in1,in2,out)
                        in1.dest = gate
                        in2.dest = gate
                        stack.append(in2)
                        stack.append(in1)
		elif id == 0:
			pass
		elif id % 2 == 1 and id > 2:
			dict[id+1] = new Fan(0,out,0)
		elif id % 2 ==0 and id > 2:
			gate = dict[id]
			in = new Wire(0,gate)
			gate.out2 = out
			gate.in = in
			
			
