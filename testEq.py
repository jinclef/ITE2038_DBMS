import csv

def read_csv_to_set(file_path):
    """CSV 파일을 읽어서 첫 번째 행을 제외한 나머지 행들을 셋(set)으로 반환하는 함수"""
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 첫 번째 row는 건너뜀 (컬럼명)
        # 각각의 행을 튜플로 변환 후 set에 저장
        data_set = {tuple(row) for row in reader}
    return data_set

def compare_csv(file1, file2, idx):
    """두 CSV 파일을 비교하고 결과를 출력하는 함수"""
    set1 = read_csv_to_set(file1)
    set2 = read_csv_to_set(file2)

    if set1 == set2:
        print(f"{idx} - Success")
    else:
        print(f"{idx} - Fail")
        
        # 차이점 출력
        only_in_file1 = set1 - set2
        only_in_file2 = set2 - set1

        if only_in_file1:
            print(f"{file1}에만 있는 행들:")
            for row in only_in_file1:
                print(row)

        if only_in_file2:
            print(f"{file2}에만 있는 행들:")
            for row in only_in_file2:
                print(row)

# 사용 예시
# file1 = '2021006317_성지원_1_result.csv'
# file2 = '문제1_결과.csv'

for i in range(1,16):
    file1 = f'DB03_SQL/2021006317_성지원_{i}_result.csv'
    file2 = f'DB03_SQL_ANS/문제{i}_결과.csv'
    
    compare_csv(file1, file2, i)
