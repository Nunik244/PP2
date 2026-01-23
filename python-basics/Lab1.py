#1
a = input()
print("Hello,", a + "!")
#2
a = input()
b = input()
print(a + "***" + b)
#3
try:
    a = int(input())
    if(a < 0): 
        exit()
except:
    print("str")
    exit()
print("int")
#4
a = int(input())
b = int(input())
print(a + b)
#5
a = int(input())
b = int(input())
print(a//b,"\n", a/b)
#6
a = int(input())
b = int(input())
print(a**b)
#7
a = int(input())
b = int(input())
print(a%b)
#8
a = input()
b = int(input())
print(a*b)
#9
a = input()
print(len(a))
#10
a = input()
print(a.upper(), "\n" + a.lower())
#11
a = input()
print(a[0], a[-1])
#12
a = input()
print(a[2:5])
#13
a = input()
print(a[::-1])
#14
a = input()
b = input()
print(f"Hello, {a}. You are {b} years old.")
#15
a = input()
b = input()

if a.find(b):
    print("False")
else:
    print("True")
#16
a = input()
b = input()
print(a + b)
#17
a = input()
b = input()
print(b , a)
#18
a = int(input())
if (a%2 == 0):
    print("even")
else:
    print("odd")
#19
a = input()
b = input()
c = input()
a = a.replace(b , c)
print(a)
#20
a = int(input())
b = int(input())
if(a == b):
    print("equal")
elif(a > b):
    print(a)
else:
    print(b)