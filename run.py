import subprocess
import re
import statistics

def execute_and_parse():
    # 바이너리 파일 실행
    result = subprocess.run(['./test.out'], capture_output=True, text=True)
    
    # 실행 결과 출력
    output = result.stdout
    print(output)  # CLI에 출력

    # 첫 번째 줄에서 Hit와 Miss 값 추출
    first_line_match = re.search(r'Hit:\s*(\d+),\s*Miss:\s*(\d+)', output.splitlines()[0])
    if first_line_match:
        hit = int(first_line_match.group(1))
        miss = int(first_line_match.group(2))
    else:
        return None  # None 반환하여 재실행 유도

    # 두 번째 줄에서 BRANCH MISS THRESHOLD 값 추출
    second_line_match = re.search(r'BRANCH MISS THRESHOLD:\s*(\d+)', output.splitlines()[1])
    if second_line_match:
        branch_miss_threshold = int(second_line_match.group(1))
    else:
        return None  # None 반환하여 재실행 유도

    # 마지막 줄에서 Collision Generated 값과 One 값 추출
    last_line_match = re.search(r'Collision Generated:\s*(\d+)/(\d+),\s*One:\s*(\d+)', output.splitlines()[-1])
    if last_line_match:
        collision_generated = int(last_line_match.group(1))
        total_generated = int(last_line_match.group(2))
        one = int(last_line_match.group(3))
        collision_ratio = collision_generated / total_generated
        # collision_ratio가 0.95 미만이면 None 반환하여 재실행 유도
        if collision_ratio < 0.95:
            return None
    else:
        return None  # None 반환하여 재실행 유도

    return hit, miss, branch_miss_threshold, collision_generated, collision_ratio, one

# 실행 결과를 저장할 리스트 초기화
results = []

# 10번 반복 실행
while len(results) < 10:
    result = execute_and_parse()
    if result is None:
        print("Collision ratio is less than 0.95 or other parsing error. Restarting...")
        results.clear()
        continue

    # 결과 리스트에 저장
    results.append(result)

# 결과 출력
hits = [result[0] for result in results]
misses = [result[1] for result in results]

mean_hit = statistics.mean(hits)
mean_miss = statistics.mean(misses)
std_dev_hit = statistics.stdev(hits)
std_dev_miss = statistics.stdev(misses)

for i, (hit, miss, branch_miss_threshold, collision_generated, collision_ratio, one) in enumerate(results):
    print(f"Iteration {i+1}:")
    print(f"  Hit = {hit}, Miss = {miss}")
    print(f"  BRANCH MISS THRESHOLD = {branch_miss_threshold}")
    print(f"  Collision Generated = {collision_generated} ({collision_ratio*100:.2f}%), One = {one}")

print(f"Mean Hit = {mean_hit}, Standard Deviation Hit = {std_dev_hit}")
print(f"Mean Miss = {mean_miss}, Standard Deviation Miss = {std_dev_miss}")
