# 설명
- 두 개의 서로 다른 branch를 .p2align으로 15 bit align시킨 뒤 랜덤한 1만비트 값을 추출하는 공격을 수행하는 test.out
- test.out을 10번 반복 실행하여 평균 branch prediction hit/miss의 cycle 수를 측정
- 모든 정답률이 95% 이상이 나올 때까지 반복 실행
  - hit/miss 값에 노이즈가 들어가서 threshold가 잘못 설정되면 정확도가 50%으로 확 떨어짐
# 사용법
```
make align
python3 run.py
```
# 프로그램 출력
``` python
<test.out>
Hit: 176, Miss: 193                         # branch prediction hit/miss 시 branch 실행에 소요되는 시간(cycle)
BRANCH MISS THRESHOLD: 187                  # threshold = (hit + 2 * miss) / 3, 1:2가 왜 잘되는지는 모르겠으나 더 잘됨
PC of Branch 1: 0x61e1379601bb              # 첫 번째 branch 함수의 virtual address (branch를 실행하는 "함수"의 주소라서 align된건 아님)
PC of Branch 2: 0x61e13796803a              # 두 번째 branch 함수의 virtual address (branch를 실행하는 "함수"의 주소라서 align된건 아님)
Collision Generated: 9765/10000, One: 4898  # One = 만 비트 중 1의 개수, 그 중 PHT-based side-channel attack을 통해 값을 추출해낸 개수
```
``` python
<run.py>
~~~
Mean Hit = 177.8, Standard Deviation Hit = 1.398411797560202
Mean Miss = 194.8, Standard Deviation Miss = 1.398411797560202
```
