import collections
import os
import sys
import pickle 
import tensorflow as tf
import random

def myfun():
	with tf.gfile.GFile("simple-examples/data/rwout.txt", "r") as f:
		
		result =  f.read().replace("CLOSE.\r\n", "<eos>, ")

		result = result.split(", ")

		print(result[0:20])
		
	return

def myfun2():
	with tf.gfile.GFile("rwithoutc.txt", "r") as f:
		
		result =  f.read().replace("CLOSE", "<eos>, ")

		result = result.split(", ")

		print(result[1:10])
		
	return


#myfun()
#print ("-"*10)
#myfun2()


#list of strings
cleaned_list = []

def read_fuction():
	with tf.gfile.GFile("simple-examples/data/datain/ResourceWithAmountFamiliarityContext.txt", "r") as f:
		result =  f.read().split("\r\n")

		for item in result:

			item_temp = item.split(".,")

			try:
				if "GOOD" == item_temp[1]:
					cleaned_list.append(item_temp[0])
			except:
				print(item_temp)

				continue 


read_fuction()

#plit the list 

ll = len(cleaned_list)

print(ll)
trainnum = ll*0.7 

trainnum = int(trainnum)


test_sample = random.sample(range(0,len(cleaned_list)-1),200)

print(test_sample)

cleaned_list_train = []
cleaned_list_test = [] 

counter = 0 
for item in cleaned_list:
	if counter in test_sample:
		cleaned_list_test.append(item)
		
	else:
		cleaned_list_train.append(item)
	counter = counter + 1 


#cleaned_list_train = cleaned_list[0:trainnum]
#cleaned_list_test= cleaned_list[trainnum:ll]




print(len(cleaned_list_train))
print(len(cleaned_list_test))



thefile = open('ResourceWithAmountFamiliarityContext_ctrain.txt', 'w')

thefile.write('\n '.join(cleaned_list_train))

thefile.close()



thefile2 = open('ResourceWithAmountFamiliarityContext_ctest.txt', 'w')

thefile2.write('\n '.join(cleaned_list_test))

thefile2.close()


'''
thefile = open('ResourceWithAmountContext_cleaned_training.txt', 'w')

for item in cleaned_list_train:
	thefile.write("%s\n" % item)

thefile.close()

thefile = open('ResourceWithAmountContext_cleaned_testing.txt', 'w')

for item in cleaned_list_test:
		thefile.write("%s\n" % item)

thefile.close()


#ml = myfun()
#print(ml[1:40])

'''
