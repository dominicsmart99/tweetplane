from hashlib import sha256
passwords = ['hello', 'goodbye', 'good ridence', 's', '']
for p in passwords:
	print(len(sha256(p.encode('utf-8')).hexdigest()))
