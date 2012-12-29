all: scratch

scratch:
	./VMtranslator.py scratch.vm

test:
	./VMtranslator.py working/SimpleFunction.vm
	cpuemu working/test.tst

BasicLoop:
	./VMtranslator.py ProgramFlow/BasicLoop/BasicLoop.vm
	cpuemu ProgramFlow/BasicLoop/BasicLoop.tst

FibonacciSeries:
	./VMtranslator.py ProgramFlow/FibonacciSeries/FibonacciSeries.vm
	cpuemu ProgramFlow/FibonacciSeries/FibonacciSeries.tst
 
SimpleFunction:
	./VMtranslator.py FunctionCalls/SimpleFunction/SimpleFunction.vm
	cpuemu FunctionCalls/SimpleFunction/SimpleFunction.vm

