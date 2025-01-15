import json
import base64
import subprocess

input_data = {'context_id': 1139, 'vulnerable': True, 'request': {'url': '/users/login/', 'method': 'POST', 'headers': {'Content-Length': '106', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'test:8000', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache', 'Referer': 'http://test:8000/users/login', 'Cookie': 'csrftoken=Rpelp2VY9BdKgRcUkP62uWp499BdtGvf'}, 'body': "b'csrfmiddlewaretoken=URL%3D%27http%3A%2F%2F8429028968341091434.owasp.org%27&username=ZAP&password=ZAP&next='"}, 'control_flow': {0: 'context = { "navinfo": config[\'DEFAULT\'][\'CSRF\'] }'}, 'response': {'status_code': '403', 'headers': {'Content-Type': 'text/html; charset=utf-8'}}}
#json_data = json.dumps(input_data)

encoded_data = base64.b64encode(str(input_data).encode('utf-8'))
base64_data = encoded_data.decode('utf-8')

result = subprocess.run(['python3', 'test_inference.py', base64_data], capture_output=True, text=True)
output = result.stdout.strip()
if output:
    print(output)
else:
    print(result.stderr.strip())
