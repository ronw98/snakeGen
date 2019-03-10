import IAGame
import Network
import sys

if __name__=='__main__':
    individual = Network.fromLog(sys.argv[1],[24,15,4])
    game = IAGame.Game(30,30)
    game.play(individual,watched=True,frameRate=0.05,infinite=True)