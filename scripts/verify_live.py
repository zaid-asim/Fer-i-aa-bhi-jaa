import urllib.request

resp = urllib.request.urlopen('http://localhost:8080/index.html')
html = resp.read().decode('utf-8')
print('HTTP status:', resp.status)
print('Has splash element:', 'id="splash"' in html)
print('Has app shell:', 'id="app"' in html)
print('App style display none:', 'style="display:none;"' in html)
