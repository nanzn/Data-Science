lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'

# Generate a list of userid in format 'aa00' consisting of 2 lowercase and 2 digits
answer = [l1+l2+n1+n2 for l1 in lowercase for l2 in lowercase for n1 in digits for n2 in digits]
print(answer[100])

