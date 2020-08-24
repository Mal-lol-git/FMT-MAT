from time import sleep


delay_time = 0.

# 지연 시간 기록
path = r'D:\pool\FMT-MAT\WEB\log.txt'

with open(path,"r") as f:
    while True:
        where = f.tell()
        line = f.readline().strip()
        if not line:
            sleep(0.1)
            delay_time += 0.1
            f.seek(where)
            if delay_time > 10.0: # 10초 이상 지연되면 파일 출력이 끝난 것으로 간주
                print("Delay has been exceeded.")
                break
            # print('대기중')
        else:
            delay_time = 0.# reset delay time
            print(line) # already has newline

