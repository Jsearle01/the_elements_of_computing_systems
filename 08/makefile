all: BasicLoop

test:
	./VMtranslator.py test.vm

BasicLoop:
	./VMtranslator.py ProgramFlow/BasicLoop/BasicLoop.vm
	cpuemu ProgramFlow/BasicLoop/BasicLoop.tst

