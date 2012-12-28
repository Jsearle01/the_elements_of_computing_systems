all: test

test:
	./VMtranslator.py working/test.vm
	cpuemu working/test.tst

BasicLoop:
	./VMtranslator.py ProgramFlow/BasicLoop/BasicLoop.vm
	cpuemu ProgramFlow/BasicLoop/BasicLoop.tst

FibonacciSeries:
	./VMtranslator.py ProgramFlow/FibonacciSeries/FibonacciSeries.vm
	cpuemu ProgramFlow/FibonacciSeries/FibonacciSeries.tst
 
