__author__ = 'lai'

def prime():
	n=int(raw_input())

	array=[]

	for i in range(2,n):
		if is_prime(i):
			array.append(i)

	while True :
		try:
			num=int(raw_input())
			index= getIndex(array,num,0,len(array)-1)
			print index
		except:
			break

def is_prime(num):
	for i in range(2,num):
		if num%i==0:
			return False
	return True


def getIndex(array,num,low,hight):
	if low>hight:
		return -1
	else:
		mid=(low+hight)/2
		midNum=array[mid]
		if midNum==num:
			return mid
		elif midNum>num:
			return getIndex(array,num,low,mid-1)
		else:
			return getIndex(array,num,mid+1,hight)

prime()
