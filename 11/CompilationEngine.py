#! /usr/bin/env python3

import itertools

from VMWriter import VMWriter
from SymbolTable import SymbolTable

from collections import namedtuple

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

uniqueID = itertools.count(0)

def uniqueLabels(*labels):
    uid = uniqueID.__next__()
    unique_labels = ['%s_%s' % (label, uid) for label in labels]
    return unique_labels

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
                raise SyntaxError('unknown variable: {}'.format(name))
            return s

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
        skipToken()

        kind = tokenValue()
        skipKeyword('field', 'static')

        typ = tokenValue()
        skipType()

        name = tokenValue()
        skipIdentifier()

        self.classSymbols.Define(name, typ, kind)

        while tokenIs('symbol', ','):
            skipToken()

            name = tokenValue()
            skipIdentifier() # varName
            self.classSymbols.Define(name, typ, kind)

        skip('symbol', ';')

        closeTag()

    def compileSubroutine(self):

        self.subroutineSymbols.startSubroutine()

        openTag('subroutineDec')

        subroutineType = tokenValue()
        skipToken()

        # TODO implement method
        if subroutineType == 'method':
            # extra argument for 'this'
            pass

        returnType = tokenValue()

        if tokenIsKeyword('void'):
            skipToken()
        else:
            skipType()

        functionName = '{}.{}'.format(self.currentClass, tokenValue())
        skipIdentifier()

        self.subroutineTypes[functionName] = Function(subroutineType,
                returnType)

        self.compileParameterList()


        openTag('subroutineBody')
        skip('symbol', '{')

        nLocals = 0
        while tokenIsKeyword('var'):
            nLocals += self.compileVarDec()

        vmw.writeFunction(functionName, nLocals)

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

        while tokenIs('symbol', '['):
            skipToken()
            self.compileExpression()
            skip('symbol', ']')

        # TODO calculate lhs offset

        lhsSymbol = getSymbol(lhsName)

        skip('symbol', '=')

        self.compileExpression()

        # pop into lhs
        vmw.writePop(lhsSymbol.kind, lhsSymbol.index)

        skip('symbol', ';')
        closeTag()

    def compileIf(self):
        openTag('ifStatement')
        skip('keyword', 'if')

        skip('symbol', '(')
        self.compileExpression()
        skip('symbol', ')')

        if_false, if_end = uniqueLabels('if_false', 'if_end')

        vmw.WriteArithmetic('not')
        vmw.WriteIf(if_false)

        # true
        skip('symbol', '{')
        self.compileStatements()
        vmw.WriteGoto(if_end)
        skip('symbol', '}')

        vmw.WriteLabel(if_false)

        # else
        if tokenIsKeyword('else'):
            skipToken()
            skip('symbol', '{')
            self.compileStatements()
            skip('symbol', '}')

        vmw.WriteLabel(if_end)
        closeTag()

    def compileWhile(self):
        openTag('whileStatement')
        skip('keyword', 'while')

        while_start, while_end = uniqueLabels('while_start', 'while_end')

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

        name.append(tokenValue())
        skipIdentifier()

        if tokenIsSymbol('.'):
            skipToken()
            name.append(tokenValue())
            skipIdentifier()

        skip('symbol', '(')
        nArgs = self.compileExpressionList()
        skip('symbol', ')')
        skip('symbol', ';')

        vmw.writeCall('.'.join(name), nArgs)
        closeTag()

    def compileReturn(self):
        openTag('returnStatement')
        skip('keyword', 'return')
        if self.compileExpression() == 0:
            vmw.writePush('constant', 0)
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
            vmw.writePush('constant', tokenValue())
            skipToken()
        elif tokenIsType('stringConstant'):
            # TODO stringConstant
            skipToken()
        elif tokenIsKeyword('true', 'false', 'null', 'this'):
            value = tokenValue()
            if value == 'true':
                vmw.writePush('constant', 1)
                vmw.WriteArithmetic('neg')
            else:
                vmw.writePush('constant', 0)
            skipToken()
        elif tokenIsKeyword('this'):
            # TODO this
            skipToken()
        elif tokenIsType('identifier'):
            identifierValue = tokenValue()
            skipToken()
            if tokenIs('symbol', '['):
                # varName [ expression ]
                skipToken()
                self.compileExpression()
                skip('symbol', ']')
                # TODO support multi dimension array
            elif tokenIs('symbol', '('):
                # subroutineName ( expressions )
                skipToken()

                nArgs = self.compileExpressionList()

                skip('symbol', ')')

                vmw.writeCall(identifierValue, nArgs)
            elif tokenIs('symbol', '.'):
                skipToken()

                functionName = '%s.%s' % (identifierValue, tokenValue())
                skipIdentifier()

                skip('symbol', '(')
                nArgs = self.compileExpressionList()
                skip('symbol', ')')

                vmw.writeCall(functionName, nArgs)
            else:
                # varName
                symbol = getSymbol(identifierValue)
                vmw.writePush(symbol.kind, symbol.index)
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

