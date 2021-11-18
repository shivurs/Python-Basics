def filter_longer(in_file, out_file, max_len = 8):
    inf = open(in_file, 'r')
    outf = open(out_file, 'w')
    readline = inf.readline().strip()
    while readline != '': 
        if len(readline) > int(max_len):
            outf.write(readline + '\n')
        readline = inf.readline().strip()
    inf.close()
    outf.close()
    
def count_lines(filename):
    linecount = 0
    f = open(filename)
    line = f.readline()
    while line != '':
        linecount +=1
        line = f.readline()
    f.close()
    return linecount
    

