import binascii
import os
from secretsharing import SecretSharer

'''
Method:
	generatePrivateKey
Arguments:
	database object(if one is made)
Function:
	Generates a private key. Searches the key in the database so as to return unique
	key everytime. Breaks the key using shamir's secret sharing and returns two 
	hexadecimals.

To-Do: Maintain a database for which key is assigned to which users. No two users
	   should have same private key. Here, we can do it in a pickle file or maintain
	   a database.
'''
def generatePrivateKeyPair():
	temporaryKey = binascii.b2a_hex(os.urandom(16))
	print(temporaryKey)
	keyPair = SecretSharer.split_secret(temporaryKey,2,3);
	return keyPair[0][2:],keyPair[1][2:],keyPair[2][2:]

'''
Method:
	getPrivateKey
Arguments:
	key1
	key2
	key3
Function:
	Takes arguments and returns key
'''
def getPrivateKey(key1,key2,key3):
	list = []
	list.append('1-'+key1)
	list.append('2-'+key2)
	list.append('3-'+key3)	
	key = SecretSharer.recover_secret(list[0:2])
	return key

a,b,c = generatePrivateKeyPair()
print(getPrivateKey(a,b,c))
