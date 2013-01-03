#! /usr/bin/env python3

import html

from VMWriter import VMWriter
from SymbolTable import SymbolTable

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
    indentPrint('<{0}> {1} </{0}>'.format(t, html.escape(v)))

tagStack = []

def openTag(s):
    global indentLevel
    indentPrint('<%s>' % s)
    tagStack.append(s)

def closeTag():
    global indentLevel
    s = tagStack.pop()
    indentPrint('</%s>' % s)

class CompilationEngine():
    def __init__(self, tokenizer, file_out):
        self.tokenizer = tokenizer
        self.file_out = file_out

        global vmw
        self.vmw = VMWriter(file_out)
        vmw = self.vmw

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
        global skipIdentifier, indentPrint

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

        def indentPrint(s):
            return
            indent = len(tagStack) * '  '
            print(indent + s, file=file_out)

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

        skipType()
        skipIdentifier()

        while tokenIs('symbol', ','):
            skipToken()
            skipIdentifier() # varName

        skip('symbol', ';')

        closeTag()

    def compileSubroutine(self):
        openTag('subroutineDec')
        skipToken()

        if tokenIsKeyword('void'):
            skipToken()
        else:
            skipType()

        functionName = '{}.{}'.format(self.currentClass, tokenValue())
        # functionName = tokenValue()
        skipIdentifier()

        nArgs = self.compileParameterList()

        vmw.writeFunction(functionName, nArgs)

        self.compileSubroutineBody()

        closeTag()

    def compileSubroutineBody(self):
        openTag('subroutineBody')
        skip('symbol', '{')

        while tokenIsKeyword('var'):
            self.compileVarDec()

        self.compileStatements()

        skip('symbol', '}')
        closeTag()

    def compileParameterList(self):
        count = 0
        skip('symbol', '(')
        openTag('parameterList')

        if not tokenIsSymbol(')'):
            skipType()
            skipIdentifier()

            count += 1

            while tokenIs('symbol', ','):
                skipToken()
                skipType()
                skipIdentifier() # varName
                count += 1

        closeTag()
        skip('symbol', ')')
        return count

    def compileVarDec(self):
        openTag('varDec')
        skipToken()

        skipType()
        skipIdentifier()

        while tokenIs('symbol', ','):
            skipToken()
            skipIdentifier() # varName

        skip('symbol', ';')

        closeTag()

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
        skipIdentifier()

        while tokenIs('symbol', '['):
            skipToken()
            self.compileExpression()
            skip('symbol', ']')

        skip('symbol', '=')
        self.compileExpression()
        skip('symbol', ';')
        closeTag()

    def compileIf(self):
        openTag('ifStatement')
        skip('keyword', 'if')
        skip('symbol', '(')
        self.compileExpression()
        skip('symbol', ')')
        skip('symbol', '{')
        self.compileStatements()
        skip('symbol', '}')
        if tokenIsKeyword('else'):
            skip('symbol', '{')
            self.compileStatements()
            skip('symbol', '}')
        closeTag()

    def compileWhile(self):
        openTag('whileStatement')
        skip('keyword', 'while')
        skip('symbol', '(')
        self.compileExpression()
        skip('symbol', ')')
        skip('symbol', '{')
        self.compileStatements()
        skip('symbol', '}')
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
            skipToken()
        elif tokenIsKeyword('true', 'false', 'null', 'this'):
            skipToken()
        elif tokenIsType('identifier'):
            skipToken()
            if tokenIs('symbol', '['):
                # varName [ expression ]
                skipToken()
                self.compileExpression()
                skip('symbol', ']')
            elif tokenIs('symbol', '('):
                # subroutineName ( expressions )
                skipToken()
                self.compileExpression()
                skip('symbol', ')')
                pass
            elif tokenIs('symbol', '.'):
                skipToken()
                skipIdentifier()
                skip('symbol', '(')
                self.compileExpressionList()
                skip('symbol', ')')
            else:
                # varName
                pass
        elif tokenIs('symbol', '('):
            # subroutineName ( expressions )
            skipToken()
            self.compileExpression()
            skip('symbol', ')')
            pass
        elif tokenIsSymbol('-~'):
            skipToken()
            self.compileTerm()
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

