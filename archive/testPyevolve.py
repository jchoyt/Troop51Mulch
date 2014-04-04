from pyevolve import G1DBinaryString
from pyevolve import GSimpleGA
from pyevolve import Mutators


def evaluate( genome ):
    "Method to evaulate a genome"
    total = 500;
    count = 0;
    for gene in genome:
        if ( count % 2 == 1 ):
            total = total - gene
        else:
            total = total + gene
        count = count + 1;
    return total

genome = G1DBinaryString.G1DBinaryString(250)
genome.evaluator.set( evaluate )
genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
genome.mutator.set(Mutators.G1DListMutatorSwap)
ga = GSimpleGA.GSimpleGA(genome)
# ga.setGenerations(1000)
# ga.setMutationRate(0.05)
ga.evolve(freq_stats=10)
print ga.bestIndividual()




