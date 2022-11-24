import cProfile
import pstats
import io


def my_func():
    result = []
    for i in range(10000):
        result.append(i)

    return result


pr = cProfile.Profile()
pr.enable()

my_result = my_func()

pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('tottime')
ps.print_stats()

with open('test.txt', 'w+') as f:
    f.write(s.getvalue())
