import os

class IJKCodeGenerator:
    def __init__(self, filename, gen, ver, debug):
        self.debug = debug
        self.version = ver
        self.gen = gen
        self.filename = filename
        self.externs = ''''''
        self.code = '''_start:\n'''
        self.data = ''''''
        self.variables = {}
        self.printfn = '''_print:
    ; rdi - message
    ; ebx - lenght
    sub  rsp, 40
    mov  rcx, [rel desc]
    mov  rdx, rdi
    mov  r8d, ebx
    xor  r9, r9
    mov  qword [rsp + 32], 0
    call WriteFile
    add  rsp, 40
    ret

_printNl:
    ; printing new line
    push rbx
    push rdi
    lea rdi, [rel nl]
    mov ebx, 2
    call _print
    pop rdi
    pop rbx
    ret

'''
        self.handle = '''   ; get console window descriptor
    mov  rcx, -11
    call GetStdHandle
    mov  [rel desc], rax
'''

    def filebase(self):
        return f'''; (c) IJKLang Compiler v{self.version}
; DO NOT MODIFY

; THIS LANGUAGE IN BETA! 
; MANY BUGS ARE NOT FIXED YET!

{self.externs}
    
section .data
{self.data}
section .text
jmp _start
{self.code}
    '''

    def writefn(self, mesn, lenght):
        return f'''
    lea rdi, [rel {mesn}]
    mov ebx, {lenght}
    call _print
    call _printNl
'''

    def generate_file(self):
        with open(self.filename + '.asm', 'w') as file:
            file.write(self.file)

    def generate(self, text):
        if self.debug:
            print('-'*40, '\n', 'CODEGEN DEBUG OUTPUT', '\n', '-'*40, '\n')
        for line in text:
            if self.debug and not line == '':
                print('AST command: ', line)
            if line == 'CINIT':
                prc = 0
                self.code = self.printfn + self.code
                self.code += self.handle
                self.data += f'''nl: db 13, 10\ndesc: dq 0\n'''
                self.externs += '''extern GetStdHandle\nextern WriteFile'''
            elif 'WRITE:' in line:
                if '$' in line[6::]:
                    if self.variables[line[7::]].isdigit():
                        print('Digits are unavailable in output yet!')
                        return
                    else:
                        self.code += self.writefn(f'{line[7::]}', len(self.variables[line[7::]]))
                else:
                    if line[6::].isdigit():
                        prc += 1
                        self.data += f'''message{prc}: db "{line[6::]}"\n'''
                        self.code += self.writefn(f'message{prc}', len(line[6::]))
                    else:
                        prc += 1
                        self.data += f'''message{prc}: db {line[6::]}\n'''
                        self.code += self.writefn(f'message{prc}', len(line[7:-1:]))
            elif 'VARIABLE:' in line:
                self.variables[line[9:line.find('::'):]] = line[line.find('::')+2::]
                self.data += f'''{line[9:line.find('::'):]}: db {line[line.find('::')+2::]}\n'''
            elif 'RETURN:' in line:
                self.code += f'''\tmov rax, {line[7::]}\n\tret'''
            elif 'SUM:' in line:
                self.code += f'''\tmov rax, {line[4:line.find('::'):] if not line[4:line.find('::'):] in self.variables else f'[rel {line[4:line.find('::'):]}]'}\n\tadd rax, {line[line.find('::')+2:line.find(':::'):] if line[line.find('::')+2:line.find(':::'):] not in self.variables else f'[rel {line[line.find('::')+2:line.find(':::'):]}]'}\n\tmov [rel {line[line.find(':::')+3::]}], rax\n'''
            elif 'SUB:' in line:
                self.code += f'''\tmov rax, {line[4:line.find('::'):] if not line[4:line.find('::'):] in self.variables else f'[rel {line[4:line.find('::'):]}]'}\n\tsub rax, {line[line.find('::')+2:line.find(':::'):] if line[line.find('::')+2:line.find(':::'):] not in self.variables else f'[rel {line[line.find('::')+2:line.find(':::'):]}]'}\n\tmov [rel {line[line.find(':::')+3::]}], rax\n'''
            elif 'INC:' in line:
                self.code += f'''\tmov rax, [rel {line[4::]}]\n\tadd rax, 1\n\tmov [rel {line[4::]}], rax\n'''
            elif 'DEC:' in line:
                self.code += f'''\tmov rax, [rel {line[4::]}]\n\tsub rax, 1\n\tmov [rel {line[4::]}], rax\n'''
        self.file = self.filebase()
        if self.debug:
            print('\n\nReady Assembly file:\n', self.file, '\n')
        if self.gen == 'exe':
            self.generate_file()
            os.system(f' nasm -f win64 {self.filename}.asm -o {self.filename}.o')
            os.system(fr'ld {self.filename}.o -o {self.filename}.exe -L C:\Windows\System32 -l kernel32 ')
            os.system(f'del {self.filename}.asm')
            os.system(f'del {self.filename}.o')
        elif self.gen == 'asm':
            self.generate_file()
        elif self.gen == 'obg':
            self.generate_file()
            os.system(f' nasm -f win64 {self.filename}.asm -o {self.filename}.o')
            os.system(f'del {self.filename}.asm')
        elif self.gen == 'all':
            self.generate_file()
            os.system(f' nasm -f win64 {self.filename}.asm -o {self.filename}.o')
            os.system(fr'ld {self.filename}.o -o {self.filename}.exe -L C:\Windows\System32 -l kernel32 ')

