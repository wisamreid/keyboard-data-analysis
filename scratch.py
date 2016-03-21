import numpy as np

# xs = np.asarray([45, 32, 52, 94, 64, 21, 67, 67])
# ys = np.asarray([67, 94])
# ndx = np.asarray([np.nonzero(xs == y)[0][0] for y in ys]) # <---- This line
# print(ndx)

# nameArr = ['josh','is','a','person', 'a', 'a',]
# Using map
# map(nameArr.index, ['a', 'is'])
# Using list comprehensions
# yo = [nameArr.index(x) for x in ['a', 'is']]
# print yo

d = dict(zip(nameArr, range(len(nameArr))))
items = ['a','is']
print [d.get(x, None) for x in items]


# moving average
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
Z = np.arange(20)
print(moving_average(Z, n=3))

from inspect import currentframe, getframeinfo

# print line numbers outside of a function
frameinfo = getframeinfo(currentframe())
print frameinfo.filename, frameinfo.lineno + 1 # line number follows frameinfo declarartion

# print line numbers inside of a function
def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

print "This is line 7, python says line ", get_linenumber()

# size 3 sliding window 
nums = [1, 3, 5, 6, 7, 8, 9, 10, 15, 19, 20, 22, 23, 24, 26, 27, 28, 32, 33, 35, 37, 38, 39, 40, 41, 42, 43, 44, 47, 48]
[nums[i:i+3] for i in xrange(len(nums))]
