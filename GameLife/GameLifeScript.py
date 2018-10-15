import sys
import argparse
import GameLifeLibrary as Lib

parser = argparse.ArgumentParser(description='Input/output characteristic')
parser.add_argument('-infile', action='store', dest='infile')
parser.add_argument('-outfile', action='store', dest='outfile')
args = parser.parse_args()

instream = sys.stdin
outstream = sys.stdout
if (args.infile):
    instream = open(args.infile, 'rt')
if (args.outfile):
    outstream = open(args.outfile, 'wt')
n, m, k = map(int, instream.readline().split())
field = [list(instream.readline()) for i in range(n)]

game = Lib.GameLife(n, m, k, field)
game.Run(outstream)
