# memory-page-backend

## 세팅하기

``` bash
poetry install # 종속성 변경 사항 불러오기
poetry add {name} # 종속성 설치
poetry run python3 test.py # poetry를 사용한 실행
```

## 병렬 테스트 수행

```bash
poetry run pytest . -n auto --asyncio-mode=auto
```
