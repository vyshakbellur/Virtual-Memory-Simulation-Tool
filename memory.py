import sys
import random as ran
import numpy as np

class memoryRequests:
	def __init__(self,process, intent, address,arrival, repeat,refer):
		self.process = process
		self.intent = intent
		self.address = address
		self.arrival = arrival
		self.repeat = repeat
		self.refer = refer
		
class mainMemory:
	memory = []
	def __init__(self, memoryRequests):
		self.memoryRequests = memoryRequests
	
	def __iter__(self):
		return self
		
	def getLeastFrequent():
		lf = mainMemory.memory[0]
		#print([mem.repeat for mem in mainMemory.memory])
		lf = mainMemory.memory[0]
		for m in mainMemory.memory:
			if m.arrival < lf.arrival:
				lf = m
			if m.repeat == 0 and (m.intent == "R\n" or m.intent == "R"):
				return mainMemory.memory.index(m)
			
		return mainMemory.memory.index(lf)
		
	def periodicReferenceReset():
		lf = mainMemory.memory[0]
		for m in mainMemory.memory:
			if m.arrival < lf.arrival:
				lf = m
			if m.refer == 0 and (m.intent == "R\n" or m.intent == "R"):  #unreferenced page where the dirty bit is off
				return mainMemory.memory.index(m)
			if m.refer == 0 and (m.intent == "W\n" or m.intent == "W"): #unreferenced page where the dirty bit is on
				return mainMemory.memory.index(m)
		return mainMemory.memory.index(lf)
			
if __name__ == '__main__':
	data = sys.argv[1]
	algorithm = sys.argv[2]
	debug = sys.argv[3]

	dataOpen = open(data,'r')
	info = dataOpen.readlines()
	dataOpen.close()
	
	requestsArray = []
	time = 0
	repeat = 0
	
	pageFound = 0
	dirtyBit = 0
	pageFault = 0
	diskReference = 0
	remove = 0
	nextReq = 0
	refer = 0
	
	for det in info:
		elem = det.rsplit("\t")
		mem = memoryRequests(elem[0],elem[2],elem[1].strip(),time, repeat, refer)
		requestsArray.append(mem)
		time += 1
	
	for req in requestsArray:
		if req.arrival < 32:
			mainMemory.memory.append(req)
			pageFault += 1
			diskReference += 1
			continue
		for mem in mainMemory.memory:
			if (mem.process == req.process) and (mem.address == req.address):
				pageFound += 1
				mem.repeat += 1
				nextReq = 1
				break
		
		if nextReq == 1:
			nextReq = 0
			continue
		
		pageFault += 1	
		if algorithm == "RAND" or algorithm == "rand":
			remove = ran.randrange(0,len(mainMemory.memory))
			swapOut = mainMemory.memory[remove]
			if swapOut.intent == "W\n" or swapOut.intent == "W":
					dirtyBit += 1
					diskReference += 2
					if debug == "1":
						print("The page was dirty")
			else:
					diskReference += 1
					if debug == "1":
						print("The page was not dirty")
			mainMemory.memory[remove] = req
			if (debug == "1"):
				print("line that generated page fault:",req.arrival)
				print("process arrived",req.process, "at", req.address)
				print("process that was removed : ",swapOut.process," with address ", swapOut.address)
				print("process added :", mainMemory.memory[remove].process," with address ", mainMemory.memory[remove].address)
			continue
				
		if algorithm == "LRU" or algorithm == "lru":
			least = mainMemory.getLeastFrequent()
			swapOut = mainMemory.memory[least]
			if swapOut.intent == "W\n" or swapOut.intent == "W":
				dirtyBit += 1
				diskReference += 2
				if debug == "1":
					print("The page was dirty")
			else:
				diskReference += 1
				if debug == "1":
					print("The page was not dirty")
			mainMemory.memory[least] = req
			if debug == "1" :
				print("line that generated page fault:",req.arrival)
				print("process arrived",req.process, "at", req.address)
				print("process that was removed : ",swapOut.process," with address ", swapOut.address)
				print("process added :", mainMemory.memory[remove].process," with address ", mainMemory.memory[remove].address)
			continue
			
		if algorithm == "FIFO" or algorithm == "fifo":
			if remove == 32:
				remove = 0
			swapOut = mainMemory.memory[remove]
			if swapOut.intent == "W\n" or swapOut.intent == "W":
				dirtyBit += 1
				diskReference += 2
				if debug == "1":
					print("The page was dirty")
			else:
				diskReference += 1
				if debug == "1":
					print("The page was not dirty")
			mainMemory.memory[remove] = req
			if debug == "1" :
				print("line that generated page fault:",req.arrival)
				print("process arrived",req.process, "at", req.address)
				print("process that was removed : ",swapOut.process," with address ", swapOut.address)
				print("process added :", mainMemory.memory[remove].process," with address ", mainMemory.memory[remove].address)
			remove += 1
			continue
			
		if algorithm == "PER" or algorithm == "per":
			if diskReference%200 == 0:
				for mem in mainMemory.memory:
					mem.refer = 0
			
			remove = mainMemory.periodicReferenceReset()
			swapOut = mainMemory.memory[remove]
			
			if swapOut.intent == "W\n" or swapOut.intent == "W":
					dirtyBit += 1
					diskReference += 2
					if debug == "1":
						print("The page was dirty")
			else:
					diskReference += 1
					if debug == "1":
						print("The page was not dirty")
			mainMemory.memory[remove] = req
			mainMemory.memory[remove].refer += 1
			if debug == "1":
				print("line that generated page fault:",req.arrival)
				print("process arrived",req.process, "at", req.address)
				print("process that was removed : ",swapOut.process," with address ", swapOut.address)
				print("process added :", mainMemory.memory[remove].process," with address ", mainMemory.memory[remove].address)
			continue
				
	print("number of Page Found :",pageFound)
	print("number of page faults",pageFault)
	print("dirty bit count",dirtyBit)
	print("total disk references:", diskReference)