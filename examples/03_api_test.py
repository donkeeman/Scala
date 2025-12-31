import httpx

url = "https://jsonplaceholder.typicode.com/todos/1"

response = httpx.get(url)

print(f"Status Code: {response.status_code}")
print(f"응답 데이터: {response.json()}")