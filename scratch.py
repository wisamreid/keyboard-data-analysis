import numpy as np

# xs = np.asarray([45, 32, 52, 94, 64, 21, 67, 67])
# ys = np.asarray([67, 94])
# ndx = np.asarray([np.nonzero(xs == y)[0][0] for y in ys]) # <---- This line
# print(ndx)

nameArr = ['josh','is','a','person', 'a', 'a',]
# Using map
# map(nameArr.index, ['a', 'is'])
# Using list comprehensions
# yo = [nameArr.index(x) for x in ['a', 'is']]
# print yo

d = dict(zip(nameArr, range(len(nameArr))))
items = ['a','is']
print [d.get(x, None) for x in items]
