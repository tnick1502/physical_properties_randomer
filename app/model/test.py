x = ["a", "b", "c", "d", "e", "f", "j", "h", "i", "j"]

left = "b"
right = 'h'

print(x[x.index(left) + 1: x.index(right)])
