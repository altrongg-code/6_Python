"""
name = input("이름 입력: ")
gender = input("성별(M/F) 입력: ")
age = input("나이 입력: ")
height = input("키 입력: ")

print(f"이름: {name}, 성별: {gender}, 나이: {age}, 키: {height}cm")
"""

"""
lower_alphabet = input("영문 소문자를 입력하세요: ")

print(f"소문자: {lower_alphabet}")
print(f"대문자: {lower_alphabet.upper()}")
"""

"""
a = int(input("첫 번째 정수를 입력하세요: "))
b = int(input("두 번째 정수를 입력하세요: "))

print(f"합: {a+b}")
print(f"차: {a-b}")
print(f"곱: {a*b}")
print(f"몫: {a//b}")
print(f"나머지: {a%b}")
"""

"""
import math

x = int(input("첫 번째 정수를 입력하세요: "))
y = int(input("두 번째 정수를 입력하세요: "))

print(f"2의 제곱: {math.pow(x,2)}")
print(f"4의 제곱근: {math.sqrt(y)}")
"""

"""
score = int(input("점수를 입력하세요(0-100): "))
if score > 100 or score < 0:
    print("점수를 올바르게 입력해주세요.")
grade = ""
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
print(f"학점: {grade}")
"""

"""
for i in range(1, 101):
    if i % 2 == 0:
        print(i)
"""

"""
print("1부터 100까지의 숫자 중 3의 배수이거나 5의 배수가 아닌 수의 합")
sum = 0
for i in range(1, 101):
    if i % 3 == 0 and not i % 5 == 0:
        sum += i
print(f"결과: {sum}")
"""
