import subprocess
import re

def init(url, thread):
    # SQLMap 명령어
    sqlmap_command = [
        "sqlmap",
        "-u",
        url,
        "--threads=" + thread,
    ]

    return sqlmap_command

def process_run(sqlmap_command):
    # SQLMap 프로세스 실행
    process = subprocess.Popen(sqlmap_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 실행 결과 읽기
    output_lines = []
    injectable_lines = []  # might be injectable이 있는 줄 목록
    for _ in range(30):
        output_line = process.stdout.readline()
        if not output_line:
            break
        output_lines.append(output_line)
        print(output_line.strip())  # 실행 결과 한 줄씩 출력

        # might be injectable이 있는 줄 저장
        if "might be injectable" in output_line:
            injectable_lines.append(output_line.strip())

    # 프로세스 강제 종료
    process.terminate()
    process.wait()

    return output_lines, injectable_lines

def result(output_lines, injectable_lines, file_path):
    # 결과 출력
    output = ''.join(output_lines)  # 실행 결과 합치기

    # 취약점 판단을 위한 패턴
    pattern_injectable = r"might be injectable"
    pattern_not_injectable = r"does not seem to be injectable"

    # 취약점 여부 분석
    matches_injectable = re.findall(pattern_injectable, output)
    matches_not_injectable = re.findall(pattern_not_injectable, output)

    if matches_injectable:
        for line in injectable_lines:
            # 결과를 txt 파일로 저장
            with open(file_path, "w") as file:
                file.write(line)
        print(f'Saved injectable point: {file_path}')
        return 'True'

    elif matches_not_injectable:
        return 'False'
    else:
        return 'Unknown'
