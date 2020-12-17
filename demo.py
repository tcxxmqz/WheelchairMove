

a = b'1_OP:0,1,1,0,0,0\r\n'

b = [0 for i in range(18)]
for i in range(len(a)):
    b[i] = chr(a[i])
print(b)

index1, index2 = 0, 0
# for a, c in enumerate(b):
#     if c == ":":
#         index1 = a
#     elif c == "\r":
#         index2 = a
d = []
for a, c in enumerate(b):
    if c == ":":
        index1 = a
    if c in ['0', '1', '2', '3', '4', '5']:
        if a > index1:
            print(c)
            d.append(c)

print(d)
