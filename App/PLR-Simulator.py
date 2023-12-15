import logging
import sys
sys.path.insert(0, '../Lib')
import MarkovChain
from os import listdir, makedirs
from os.path import isfile, join, exists


def convertToInt(s):
    try:
        return int(s)
    except ValueError:
        logging.warning("Convert to Int:Value error %s" % s)
        return s


def convertToFloat(s):
    try:
        return float(s)
    except ValueError:
        logging.warning("Convert to Float:Value error %s" % s)
        return s


class PLRProcess():
    def __init__(self, initial_state: MarkovChain.ChannelState, p: float, r: float):
        states = [MarkovChain.ChannelState.GOOD, MarkovChain.ChannelState.BAD]
        transition_matrix = [[1 - p, p], [r, 1 - r]]
        self.ChannelSim = MarkovChain.MarkovChain(transition_matrix, states)
        self.actual_state = initial_state

    def get_next_state(self):  # Renamed method to follow Python naming convention
        self.actual_state = self.ChannelSim.next_state(self.actual_state)

    def get_actual_state(self):  # Renamed method to follow Python naming convention
        return self.actual_state


def GenerateTXRXFile(tracefile: str, txfile: str, rxfile: str, randomprocess: PLRProcess):
    print("[PLR-Noise] Generating %s %s" % (txfile, rxfile))
    with open(tracefile, "r") as trace_file, open(txfile, "w") as tx_file, open(rxfile, "w") as rx_file:  # Using multiple context managers in a single line
        for line in trace_file:  # Renamed lines to line to improve clarity
            tokens = line.split(sep="\t")
            tx_file.write("%d,udp,%d,%s,\n" % (convertToInt(tokens[0])-1, convertToInt(tokens[3]), tokens[2]))
            if (randomprocess.get_actual_state() == MarkovChain.ChannelState.GOOD):  # Renamed method to follow Python naming convention
                rx_file.write("%d,udp,%d,%s,\n" % (convertToInt(tokens[0])-1, convertToInt(tokens[3]), tokens[2]))
            randomprocess.get_next_state()  # Renamed method to follow Python naming convention


if __name__ == "__main__":
    if len(sys.argv) > 1:
        traceFile = sys.argv[1]
        pe = convertToFloat(sys.argv[2])  # Changed convertToInt to convertToFloat since you're dividing it by 100
    else:
        print("WARNING: No specific folder and PLR is set for the output file")
        sys.exit()
    process = PLRProcess(MarkovChain.ChannelState.GOOD, pe/100, 1)
    GenerateTXRXFile(traceFile, "TX_%s" % traceFile, "RX_%s" % traceFile, process)

