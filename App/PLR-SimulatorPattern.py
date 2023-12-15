import logging,sys
sys.path.insert(0, '../Lib')
from os.path import isfile, join, exists
def convertToInt(s):
    try:
        return int (s)
    except ValueError:
        logging.warning("Value error %s" %s)
        return s
def GenerateTXRXFile(tracefile:str,txfile:str,rxfile:str,signal,FirstIdx):
    print ("[PLR-Noise] Generating %s %s from %d"%(txfile,rxfile,FirstIdx))
    with open(tracefile,"r") as tracefile:
        with open(txfile,"w") as txfile:
            with open(rxfile,"w") as rxfile:
                for lines in tracefile:
                    token = lines.split(sep="\t")
                    txfile.write("%d,udp,%d,%d\n" %(convertToInt(token[0])-1,convertToInt(token[3]),convertToInt(token[2])))
                    if (signal[FirstIdx%9700]!='0'):
                        rxfile.write("%d,udp,%d,%d\n" %(convertToInt (token[0])-1,convertToInt (token[3]),convertToInt (token[2])))
                    FirstIdx+=1
if __name__ == "__main__":
    if len(sys.argv) > 3:
        traceFile = sys.argv[1]
        pe = sys.argv[2]
        FirstIdx = convertToInt(sys.argv[3])
    else:
        print("WARNING: No specific folder and PLR is set for the output file")
        sys.exit()
    signal=[]
    with open(join("q15i16/",str(pe)),"r") as lostpatternFile:
        for line in lostpatternFile:
            for c in line:
                if (c!='/n'):
                    signal +=c
    GenerateTXRXFile(traceFile,"TX_%s"%(traceFile),"RX_%s"%(traceFile),signal,FirstIdx)


    
