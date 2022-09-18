import cProfile
import new
import pstats

cProfile.run('new','restats')

p = pstats.Stats('restats')
p.sort_stats('cumulative').print_stats(10)