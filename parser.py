class IJKParser:
    def __init__(self, debug):
        self.debug = debug
        self.functions = {}

        self.cases = {'function': [['function', 'string', 'semicolon']],
                      'command': [['system', 'string', 'semicolon'], ['string', 'sum', 'sum', 'semicolon'], ['system', 'init', 'semicolon'], ['string', 'sub', 'sub', 'semicolon'], ['string', 'assign', '%expression', 'semicolon'], ['writeln', 'op1', '%expression', 'cp1', 'semicolon'], ['return', '%expression', 'semicolon'], ['variable', 'string', 'assign', '%expression', 'semicolon'], ['variable', 'char', 'assign', '%expression', 'semicolon']],
                      'expression': [['%value'], ['%value', 'sum', '%value'], ['%value', 'sub', '%value'], ['%value', 'mul', 'number'], ['number', 'div', 'number']],
                      'value': [['sc', 'string', 'sc'], ['number'], ['cc', 'char', 'cc'], ['string']],
                      }
        self.acases = {'command': [], 'expression': []}
        self.commandCases = []

    def flattenList(self, list):
        flatlist = []
        for item in list:
            if str(type(item)) == "<class 'list'>":
                for element in item:
                    if str(type(element)) == "<class 'list'>":
                        for i in element:
                            flatlist.append(i)
                    else:
                        flatlist.append(element)
            else:
                flatlist.append(item)
        return flatlist

    def cut(self, line, half):
        nline = []
        for token in line:
            nline.append(token[half])
        return nline

    def replace(self, text, word, toreplace, var):
        for line in text:
            for rep in toreplace:
                if text.count(word) == 2:
                    for rep2 in toreplace:
                        if line == word:
                            ntext = list(text)
                            ntext[ntext.index(line)] = rep2
                            ntext[ntext.index(line)] = rep
                            self.acases[var].append(ntext)
                else:
                    if line == word:
                        ntext = list(text)
                        ntext[ntext.index(line)] = rep
                        self.acases[var].append(ntext)
    def createCases(self):
        self.acases['command'] = self.cases['command']
        for case in self.cases['expression']:
            self.replace(case, '%value', self.cases['value'], 'expression')
        for case2 in self.cases['command']:
            self.replace(case2, '%expression', self.acases['expression'], 'command')
        for item in self.acases['command']:
            self.commandCases.append(self.flattenList(item))
        for command in self.commandCases:
            if self.commandCases.count(command) >= 2:
                self.commandCases.remove(command)

    def createCasesOLD(self):
        for case in self.cases['program']:
            for expression in self.cases['expression']:
                for value in self.cases['value']:
                    if '%value' in expression:
                        expression[expression.index('%value')] = value
                        print(expression)
                    if '%expression' in case:
                        case[case.index('%expression')] = expression
                    self.acases['program'].append(case)

    def parseMath(self, lline, wline, retV):
        ret = []
        if lline[1] == 'sum' and lline[2] == 'sum':
            if self.debug:
                print(f'Inc debug: {retV}')
            ret.append(f'INC:{retV}')
        elif lline[1] == 'sub' and lline[2] == 'sub':
            if self.debug:
                print(f'Dec debug: {retV}')
            ret.append(f'DEC:{retV}')
        elif 'sum' in lline:
            if self.debug:
                print(f'Sum debug: {wline[wline.index('+') - 1]}\t{wline[wline.index('+') + 1]}\t{retV}')
            ret.append(f'SUM:{wline[wline.index('+') - 1]}::{wline[wline.index('+') + 1]}:::{retV}')
        elif 'sub' in lline:
            if self.debug:
                print(f'Sub debug: {wline[wline.index('-') - 1]}\t{wline[wline.index('-') + 1]}\t{retV}')
            ret.append(f'SUB:{wline[wline.index('-') - 1]}::{wline[wline.index('-') + 1]}:::{retV}')
        elif 'mul' in lline:
            if self.debug:
                print(f'Mul debug: {wline[wline.index('*') - 1]}\t{wline[wline.index('*') + 1]}\t{retV}')
            ret.append(f'MUL:{wline[wline.index('*') - 1]}::{wline[wline.index('*') + 1]}:::{retV}')
        elif 'div' in lline:
            if self.debug:
                print(f'Div debug: {wline[wline.index("/") - 1]}\t{wline[wline.index("/") + 1]}\t{retV}')
            ret.append(f'DIV:{wline[wline.index('/') - 1]}::{wline[wline.index('/') + 1]}:::{retV}')
        return ret

    def parseFunctions(self, funcname):
        ret = []
        for line in self.functions[funcname]:
            for case in self.commandCases:
                lline = self.cut(line, 0)
                wline = self.cut(line, 1)
                if lline == case:
                    curret = ''
                    match lline[0]:
                        case 'writeln':
                            if self.parseMath(lline, wline, wline[1]) != []:
                                raise ValueError('Error: Math expressions denied in function parameters!')
                            curret = 'WRITE:'
                            if 'string' in case and not 'sc' in case:
                                curret += '$'
                            for i in wline[2:-2:]:
                                curret += str(i)
                        case 'return':
                            curret = 'RETURN:'
                            for i in wline[1:-1:]:
                                curret += str(i)
                        case 'variable':
                            curret = 'VARIABLE:' + wline[1] + '::'
                            if self.parseMath(lline, wline, wline[1]) != []:
                                ret.append(self.parseMath(lline, wline, wline[1]))
                                curret += '228'
                            else:
                                for i in wline[3:-1:]:
                                    curret += str(i)
                        case 'system':
                            if lline[1] == 'init':
                                ret.append('CINIT')
                            else:
                                ret.append(self.parseFunctions(wline[1]))
                        case 'string':
                            if self.parseMath(lline, wline, wline[0]) != []:
                                ret.append(self.parseMath(lline, wline, wline[0]))
                    ret.append(curret)
            if self.debug:
                print('Parse debug: ',line, '\t', lline, '\t', wline)
        return self.flattenList(ret)

    def recordFunctions(self, text):
        for line in text:
            wline = self.cut(line, 0)
            if wline == self.cases['function'][0]:
                lline = self.cut(line, 1)
                parens = 0
                mi = 0
                for cline in text[text.index(line)+1::]:
                    mi += 1
                    if self.debug:
                        print('Function capture: ', cline, parens)
                    if self.cut(cline,0) == ['op3']:
                        parens += 1
                        if parens == 1:
                            fp1 = mi
                    elif self.cut(cline, 0) == ['cp3']:
                        parens -= 1
                        if parens == 0:
                            fp2 = mi
                            self.functions[lline[1]] = text[fp1+1:fp2-1:]
                            break


    def parse(self, text):
        if self.debug:
            print('-'*40, '\n', 'PARSER DEBUG OUTPUT', '\n', '-'*40, '\n')
        self.createCases()
        self.recordFunctions(text)
        if self.debug:
            print('Functions: ', self.functions, '\n')
        if not 'main' in self.functions:
            raise ValueError('<main> function not found!')
        return self.parseFunctions('main')