"""
    스코프

    - 전역 변수 : 함수 외부에 선언된 변수
    - 지역 변수 : 함수 내부에 선언된 변수
"""

count = 0 # 전역 변수

def increase1():
    count = 10 # 지역변수
    print(f"count: {count}") # 10

increase1()
print(f"count: {count}") # 0

def increase2():
    global count    # global : 전역변수 사용 명시
    count += 1      # count = count + 1

increase2()
increase2()
print(f"count: {count}")

# 스코프 검색 순서 : Local -> Enclosing -> Global
data = "-- 전역 --"

def outer():
    data = '-- 바깥 함수(outer)'

    def inner():
        data = '-- 안쪽 함수(inner) --'

        print(f"** inner :: data - {data}")

    inner()
    print(f"** outer :: data - {data}")

outer()
print(f"** 전역에서 확인 :: data - {data}")
