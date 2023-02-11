import logging,sys
sys.path.insert(0, '../Lib')
import MarkovChain
from os import listdir,makedirs
from os.path import isfile, join, exists

def convertToInt(s):
    try:
        return int (s)
    except ValueError:
        logging.warning("Value error %s" %s)
        return s
class PLRProcess():
    def __init__(self,initial_state:MarkovChain.ChannelState,p:float,r:float):
        states = [MarkovChain.ChannelState.GOOD, MarkovChain.ChannelState.BAD]
        transition_matrix= [[1 - p, p], [r, 1 - r]]
        self.ChannelSim = MarkovChain.MarkovChain(transition_matrix, states)
        self.actual_state = initial_state
    def getnextState(self):
        self.actual_state = self.ChannelSim.next_state(self.actual_state)
    def getActualState(self):
        return self.actual_state
    
def GenerateTXRXFile(tracefile:str,txfile:str,rxfile:str,randomprocess:PLRProcess):
    print ("[PLR-Noise] Generating %s %s"%(txfile,rxfile))
    previous_time = 0
    with open(tracefile,"r") as tracefile:
        with open(txfile,"w") as txfile:
            with open(rxfile,"w") as rxfile:
                for lines in tracefile:
                    token = lines.split(sep="\t")
                    txfile.write("%d,udp,%d,%d\n" %(convertToInt(token[0])-1,convertToInt(token[3]),convertToInt(token[2])))
                    if (randomprocess.getActualState() == MarkovChain.ChannelState.GOOD):
                        rxfile.write("%d,udp,%d,%d\n" %(convertToInt (token[0])-1,convertToInt (token[3]),convertToInt (token[2])))
                    previous_time = convertToInt(token[2])
                    randomprocess.getnextState()
if __name__ == "__main__":
    if len(sys.argv) > 1:
        traceFile = sys.argv[1]
        pe = convertToInt (sys.argv[2])
    else:
        print("WARNING: No specific folder and PLR is set for the output file")
        sys.exit()
    process = PLRProcess(MarkovChain.ChannelState.GOOD, pe/100, 1)
    GenerateTXRXFile(traceFile,"TX_%s"%(traceFile),"RX_%s"%(traceFile),process)

    
