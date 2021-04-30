import tensorflow as tf



#implement model 
y = tf.nn.softmax(tf.matmul(x, W) + b)

#a graph of interacting operations that run entirely outside Python
#We describe these interacting operations by manipulating symbolic variables. Let's create one:

x = tf.placeholder(tf.float32, [None, 784])


#Training
y_ = tf.placeholder(tf.float32, [None, 10])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

#initialize variables 

init = tf.initialize_all_variables()

#launch model in a session
sess = tf.Session()
sess.run(init)

#Evaluating Our Model

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))


accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
