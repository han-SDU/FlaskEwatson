import pstats
p = pstats.Stats('profiling')
# skip strip_dirs() if you want to see full path's
p.strip_dirs().sort_stats('tottime').print_stats(25)
p.strip_dirs().sort_stats('cumulative').print_stats(25)
