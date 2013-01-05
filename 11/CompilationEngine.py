#! /usr/bin/env python3

from VMWriter import VMWriter
from SymbolTable import SymbolTable

from collections import namedtuple, Counter

Function = namedtuple('Function', ['type', 'returnType'])

expressionCommands = {
        '+' : 'add',
        '-' : 'sub',
        '=' : 'eq',
        '>' : 'gt',
        '<' : 'lt',
        '&' : 'and',
        '|' : 'or',
        }


def tag(t, v):
    indentPrint('({0} {1})'.format(t, v))

tagStack = []

def openTag(s):
    global indentLevel
    indentPrint('(%s' % s)
    tagStack.append(s)

def closeTag():
    global indentLevel
    s = tagStack.pop()
    indentPrint(')')

class CompilationEngine():
    def __init__(self, tokenizer, file_out, debug=False):
        self.tokenizer = tokenizer
        self.file_out = file_out

        self.classSymbols = SymbolTable(file_out, debug)
        self.subroutineSymbols = SymbolTable(file_out, debug)
        self.subroutineTypes = {}

        self.nClassFields = 0

        global vmw
        vmw = self.vmw = VMWriter(file_out)

        global token, advance, expected, tokenValue
        global tokenIn, tokenIs, tokenIsType, tokenIsKeyword
        global tokenIsSymbol

        token          = self.tokenizer.token
        advance        = self.tokenizer.advance
        expected       = self.tokenizer.expected
        tokenValue     = self.tokenizer.tokenValue
        tokenIn        = self.tokenizer.tokenIn
        tokenIs        = self.tokenizer.tokenIs
        tokenIsType    = self.tokenizer.tokenIsType
        tokenIsKeyword = self.tokenizer.tokenIsKeyword
        tokenIsSymbol  = self.tokenizer.tokenIsSymbol

        global skip, skipToken, skipType, printToken
        global skipIdentifier, indentPrint, getSymbol
        global isMethod, getSegment, getThis, uniqueLabel
        global push, pop, call

        def uniqueLabel(label):
            uid = self.labelCounter[label]
            self.labelCounter[label] += 1
            return '%s%s' % (label, uid)

        def skip(t, v):
            self.tokenizer.skip(t, v)
            tag(t, v)

        def skipToken():
            t, v, _, _ = token()
            skip(t, v)

        def skipType():
            keywords = ('int', 'char', 'boolean')
            if tokenIsKeyword(*keywords):
                skipToken()
            elif tokenIsType('identifier'):
                skipToken()
            else:
                expected('type')

        def skipIdentifier():
            if tokenIsType('identifier'):
                skipToken()
            else:
                expected('type')

        def printToken():
            t, v, _, _ = token()
            tag(t, v)

        if debug == True:
            def indentPrint(s):
                indent = len(tagStack) * '  '
                print(indent + s, file=file_out)
        else:
            def indentPrint(s):
                pass

        def getSymbol(name):
            s = self.subroutineSymbols.Symbol(name)
            if s is None:
                s = self.classSymbols.Symbol(name)
            if s is None:
                raise KeyError('unknown variable: {}'.format(name))
            return s

        def getThis(name):
            try:
                return getSymbol(name)
            except KeyError:
                return None

        def call(lhsName, functionName, nArgs):
            if lhsName:
                this = getThis(lhsName)
                if this:
                    nArgs += 1
                    push(this.kind, this.index)
                    callName = '%s.%s' % (this.typ, functionName)
                else:
                    callName = '%s.%s' % (lhsName, functionName)
            else:
                push('pointer', 0)
                nArgs += 1
                callName = '%s.%s' % (self.currentClass, functionName)
            vmw.writeCall(callName, nArgs)

        def getSegment(kind):
            if kind == 'field':
                return 'this'
            else:
                return kind

        def pop(kind, index):
            segment = getSegment(kind)
            vmw.writePop(segment, index)

        def push(kind, index):
            segment = getSegment(kind)
            vmw.writePush(segment, index)

    def compileClass(self):
        openTag('class')
        skip('keyword', 'class')

        self.currentClass = tokenValue()
        tokenIsType('identifier')

        printToken()
        advance()

        skip('symbol', '{')

        while tokenIsKeyword('static', 'field'):
            self.compileClassVarDec()

        while tokenIsKeyword('constructor', 'function', 'method'):
            self.compileSubroutine()

        skip('symbol', '}')

        closeTag()

    def compileClassVarDec(self):
        openTag('classVarDec')

        kind = tokenValue()
        skipToken()

        typ = tokenValue()
        skipType()

        if kind == 'field': self.nClassFields += 1
        name = tokenValue()
        skipIdentifier()

        self.classSymbols.Define(name, typ, kind)

        while tokenIs('symbol', ','):
            skipToken()

            if kind == 'field': self.nClassFields += 1
            name = tokenValue()
            skipIdentifier() # varName
            self.classSymbols.Define(name, typ, kind)

        skip('symbol', ';')

        closeTag()

    def compileSubroutine(self):

        self.subroutineSymbols.startSubroutine()
        self.labelCounter = Counter()

        openTag('subroutineDec')

        subroutineType = tokenValue()
        skipToken()

        returnType = tokenValue()

        if tokenIsKeyword('void'):
            skipToken()
        else:
            skipType()

        functionName = '{}.{}'.format(self.currentClass, tokenValue())
        skipIdentifier()

        self.subroutineTypes[functionName] = Function(subroutineType,
                returnType)

        if subroutineType == 'method':
            self.subroutineSymbols.Define('this', self.currentClass, 'argument')

        self.compileParameterList()


        openTag('subroutineBody')
        skip('symbol', '{')

        nLocals = 0

        while tokenIsKeyword('var'):
            nLocals += self.compileVarDec()

        vmw.writeFunction(functionName, nLocals)

        if subroutineType == 'method':
            # set this
            push('argument', 0)
            pop('pointer', 0)
        elif subroutineType == 'constructor':
            push('constant', self.nClassFields)
            vmw.writeCall('Memory.alloc', 1)
            pop('pointer', 0)
        else:
            # do nothing for functions
            pass

        self.compileStatements()

        skip('symbol', '}')

        closeTag()

        closeTag()


    def compileParameterList(self):
        count = 0
        skip('symbol', '(')
        openTag('parameterList')

        if not tokenIsSymbol(')'):
            typ = tokenValue()
            skipType()

            name = tokenValue()
            skipIdentifier()
            
            self.subroutineSymbols.Define(name, typ, 'argument')

            count += 1

            while tokenIs('symbol', ','):
                skipToken()

                typ = tokenValue()
                skipType()

                name = tokenValue()
                skipIdentifier() # varName

                self.subroutineSymbols.Define(name, typ, 'argument')

                count += 1

        closeTag()
        skip('symbol', ')')
        return count

    def compileVarDec(self):
        nVars = 0
        openTag('varDec')
        skipToken()

        typ = tokenValue()
        skipType()

        name = tokenValue()
        skipIdentifier()
        nVars += 1

        self.subroutineSymbols.Define(name, typ, 'local')

        while tokenIs('symbol', ','):
            skipToken()
            name = tokenValue()
            skipIdentifier() # varName
            self.subroutineSymbols.Define(name, typ, 'local')
            nVars += 1

        skip('symbol', ';')

        closeTag()
        return nVars

    def compileStatements(self):
        openTag('statements')

        while tokenIsKeyword('let', 'if', 'while', 'do', 'return'):
            value = tokenValue()
            if value == 'let':
                self.compileLet()
            elif value == 'if':
                self.compileIf()
            elif value == 'while':
                self.compileWhile()
            elif value == 'do':
                self.compileDo()
            elif value == 'return':
                self.compileReturn()
            else:
                expected('statement')

        closeTag()

    def compileLet(self):
        openTag('letStatement')
        skip('keyword', 'let')

        lhsName = tokenValue()
        skipIdentifier()

        arrayFound = False

        while tokenIs('symbol', '['):
            arrayFound = True
            symbol = getSymbol(lhsName)
            skipToken()
            self.compileExpression()
            skip('symbol', ']')

            push(symbol.kind, symbol.index)
            vmw.WriteArithmetic('add')

        lhsSymbol = getSymbol(lhsName)

        skip('symbol', '=')

        self.compileExpression()

        # pop into lhs
        if arrayFound:
            pop('temp', 0)
            pop('pointer', 1)
            push('temp', 0)
            pop('that', 0)
        else:
            pop(lhsSymbol.kind, lhsSymbol.index)

        skip('symbol', ';')
        closeTag()

    def compileIf(self):
        openTag('ifStatement')
        skip('keyword', 'if')

        skip('symbol', '(')
        self.compileExpression()
        skip('symbol', ')')

        if_true = uniqueLabel('IF_TRUE')
        if_false = uniqueLabel('IF_FALSE')
        if_end = uniqueLabel('IF_END')

        vmw.WriteIf(if_true)
        vmw.WriteGoto(if_false)
        vmw.WriteLabel(if_true)

        # true
        skip('symbol', '{')
        self.compileStatements()
        skip('symbol', '}')

        # else
        if tokenIsKeyword('else'):
            vmw.WriteGoto(if_end)
            vmw.WriteLabel(if_false)

            skipToken()
            skip('symbol', '{')
            self.compileStatements()
            skip('symbol', '}')

            vmw.WriteLabel(if_end)
        else:
            vmw.WriteLabel(if_false)


        closeTag()

    def compileWhile(self):
        openTag('whileStatement')
        skip('keyword', 'while')

        while_start = uniqueLabel('WHILE_EXP')
        while_end = uniqueLabel('WHILE_END')

        vmw.WriteLabel(while_start)

        skip('symbol', '(')
        self.compileExpression()
        skip('symbol', ')')

        vmw.WriteArithmetic('not')
        vmw.WriteIf(while_end)

        skip('symbol', '{')
        self.compileStatements()
        skip('symbol', '}')

        vmw.WriteGoto(while_start)
        vmw.WriteLabel(while_end)

        closeTag()

    def compileDo(self):
        openTag('doStatement')
        skip('keyword', 'do')
        name = []

        identifier = tokenValue()
        skipIdentifier()

        if tokenIsSymbol('.'):
            skipToken()
            lhs = identifier
            functionName = tokenValue()
            skipIdentifier()
        else:
            # method call
            lhs = None
            functionName = identifier

        skip('symbol', '(')
        nArgs = self.compileExpressionList()
        skip('symbol', ')')
        skip('symbol', ';')

        call(lhs, functionName, nArgs)
        pop('temp', 0)
        closeTag()

    def compileReturn(self):
        openTag('returnStatement')
        skip('keyword', 'return')
        if self.compileExpression() == 0:
            push('constant', 0)
        vmw.writeReturn()
        skip('symbol', ';')
        closeTag()

    def compileExpression(self):
        if tokenIsSymbol(');'):
            return 0
        openTag('expression')
        self.compileTerm()
        while tokenIsSymbol('+-*/&|<>='):
            v = tokenValue()
            skipToken()
            self.compileTerm()
            if v in expressionCommands:
                vmw.WriteArithmetic(expressionCommands[v])
            elif v == '*':
                vmw.writeCall('Math.multiply', 2)
            elif v == '/':
                vmw.writeCall('Math.divide', 2)
            else:
                raise SyntaxError(v)
        closeTag()
        return 1

    def compileTerm(self):
        openTag('term')

        if tokenIsType('integerConstant'):
            push('constant', tokenValue())
            skipToken()
        elif tokenIsType('stringConstant'):
            value = tokenValue()
            skipToken()

            push('constant', len(value))
            call('String', 'new', 1)

            for c in value:
                push('constant', ord(c))
                call('String', 'appendChar', 2)
        elif tokenIsKeyword('true', 'false', 'null'):
            value = tokenValue()
            if value == 'true':
                push('constant', 0)
                vmw.WriteArithmetic('not')
            else:
                push('constant', 0)
            skipToken()
        elif tokenIsKeyword('this'):
            push('pointer', 0)
            skipToken()
        elif tokenIsType('identifier'):
            identifierValue = tokenValue()
            skipToken()
            if tokenIs('symbol', '['):
                # varName [ expression ]
                skipToken()
                self.compileExpression()
                skip('symbol', ']')

                symbol = getSymbol(identifierValue)
                push(symbol.kind, symbol.index)
                vmw.WriteArithmetic('add')

                pop('pointer', 1)
                push('that', 0)

                # TODO support multi dimension array
            elif tokenIs('symbol', '('):
                # subroutineName ( expressions )
                skipToken()

                nArgs = self.compileExpressionList()

                skip('symbol', ')')

                call(None, identifierValue, nArgs)
            elif tokenIs('symbol', '.'):
                skipToken()

                rhs = tokenValue()
                skipIdentifier()

                skip('symbol', '(')
                nArgs = self.compileExpressionList()
                skip('symbol', ')')

                call(identifierValue, rhs, nArgs)
            else:
                # varName
                symbol = getSymbol(identifierValue)
                push(symbol.kind, symbol.index)
        elif tokenIs('symbol', '('):
            skipToken()
            self.compileExpression()
            skip('symbol', ')')
        elif tokenIsSymbol('-~'):
            v = tokenValue()
            skipToken()
            self.compileTerm()
            if v == '-':
                vmw.WriteArithmetic('neg')
            else:
                vmw.WriteArithmetic('not')
        else:
            raise SyntaxError(token())

        closeTag()

    def compileExpressionList(self):
        count = 0
        openTag('expressionList')
        count += self.compileExpression()

        while tokenIs('symbol', ','):
            skipToken()
            self.compileExpression()
            count += 1

        closeTag()
        return count

