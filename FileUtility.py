from secretsharing import PlaintextToHexSecretSharer
from secretsharing import SecretSharer
import time
'''
TO-DO: Parallelize the method, it is computation extensive

Method:
	shamirs_split
Args:
	file object 
	threshold value(n)
	number of splits
Function:
	This method splits the text content of the file using shamir's secret
	sharing algorithm. A list of hex codes are generated. These hex codes
	are later broken into three parts again. This list of list is returns
	as output
'''
def shamirs_split(file_object, n, splits):
	text = file_object.read()
	if(n<splits):
		list = PlaintextToHexSecretSharer.split_secret(text,n,splits)
	else:
		return []
	print(list)
	for itr in range(splits):
		hexcode = SecretSharer.split_secret(list[itr][2:],2,3);
		list[itr] = hexcode
	print("Hexcode->")
	print(list)
	return list
'''
Method:
	shamir's join
Args:
	list
Function:
	Converts the excrypted hexcodes into decrypted ones. Use those decrypted 
	hexcode to decrypt the text. Returns the text.
'''
def shamirs_join(list):
	l = len(list)
	temp = []
	for itr in range(l):
		hexcode = SecretSharer.recover_secret(list[itr][0:2])
		temp.append(str(itr+1)+'-'+hexcode)
	text = PlaintextToHexSecretSharer.recover_secret(temp[0:l-1])
	return text
		
def main():
	t = time.time()
	#Print list to see the encrypted file!
	list = shamirs_split(open("textfile.txt","r"),2,3)
	print(shamirs_join(list))
	s = time.time()
	print("Time elapsed: %f seconds"%(s-t))

if __name__ == "__main__":
	main()

