import typer

# cli 실행 시, 필수는 인자명 없이 순서대로, 옵셔널은 --인자명 값
def main(name: str, age: int = 20):
    print(f"안녕하세요 {name}님, {age}살이시군요!")

# __name__은 파일 경로. 직접 실행 시에는 __name__이 __main__ 이므로 그거 검사, 다른 파일에서 import해온 모듈을 실행하는 경우 __name__은 파일명
# 그러므로 외부에서는 이거 실행 안 됨 -> 테스트용으로 주로 사용
if(__name__ == "__main__"): 
    typer.run(main)