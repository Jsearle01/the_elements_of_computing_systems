destinations = {}
destinations ['null'] = '000'
destinations ['M']    = '001'
destinations ['D']    = '010'
destinations ['MD']   = '011'
destinations ['A']    = '100'
destinations ['AM']   = '101'
destinations ['AD']   = '110'
destinations ['AMD']  = '111'

jumps = {}
jumps ['null'] = '000'
jumps ['JGT']  = '001'
jumps ['JEQ']  = '010'
jumps ['JGE']  = '011'
jumps ['JLT']  = '100'
jumps ['JNE']  = '101'
jumps ['JLE']  = '110'
jumps ['JMP']  = '111'

computations = {}
computations [  '0'] = '101010'
computations [  '1'] = '111111'
computations [ '-1'] = '111010'
computations [  'D'] = '001100'
computations [  'A'] = '110000'
computations [ '!D'] = '001101'
computations [ '!A'] = '110001'
computations [ '-D'] = '001111'
computations [ '-A'] = '110011'
computations ['D+1'] = '011111'
computations ['A+1'] = '110111'
computations ['D-1'] = '001110'
computations ['A-1'] = '110010'
computations ['D+A'] = '000010'
computations ['D-A'] = '010011'
computations ['A-D'] = '000111'
computations ['D&A'] = '000000'
computations ['D|A'] = '010101'

def dest(s):
    return destinations[s]

def comp(s):
    if s.find('M') >= 0:
        return '1' + computations[s.replace('M','A')]
    else:
        return '0' + computations[s]

def jump(s):
    return jumps[s]

if __name__ == "__main__":
    print("hello")
