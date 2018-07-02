from Crypto.Hash import MD2

str = 'hello'
h = MD2.new("1")
h.update(str.encode('ascii'))
temp = h.hexdigest()
print(temp)