import numpy as np

y  = np.array([1,2,3.5,10,20])

print y

#--------------------------------------

t = np.ones([5,5])

print t


#--------------------------------------

import tensorflow as tf
sess = tf.InteractiveSession()

state = tf.variable(0,name="counter")

new_value = tf.add(state,tf.constant(1))

update = tf.assign(state,new_value)

with tf.session() as sess:
	sess.run(tf.initialize_all_variables())
	print(sess.run(state))
	for _ in range(3):
		sess.run(update)
		print(sess.run(state))