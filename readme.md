# AsiaYo testing
## Run
1. Clone this repo
2. cp app/.env.example app/.env
3. docker build -t myapp . && docker run -p 80:80 myapp

## 程式說明
1. http://0.0.0.0/docs 可以參考 swagger 文檔
2. 使用 .env 的帳號密碼登入
3. /api/currency/_convert_currency 可以轉換貨幣

## 格式說明
### 成功
```
{msg: 'success', amount: 100}
```
### 失敗
```
status code is 400
{msg: 'fail', error: 'error message'}
```

## 測試
```
export PYTHONPATH=/path/to/your/project/app:$PYTHONPATH
pytest  tests
```