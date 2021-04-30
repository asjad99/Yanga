filename_queue = tf.train.string_input_producer(["file0.csv", "file1.csv"])



LEARNING_RATE_DECAY_FACTOR = 0.1  # Learning rate decay factor.
INITIAL_LEARNING_RATE = 0.1       # Initial learning rate.

def read_dataset(filename_queue):
"""
Reads and parses examples from Patari_dataset.

Args:
    filename_queue: A queue of strings with the filenames to read from.
Returns:
    An object representing a single example, with the following fields:

"""
	
	#reader = tf.SomeReader()
	
	#key,record_string = reader.read(filename_queue)
	
	#-----------------------------------
	#decode and process 
	#example,label = tf.some_decorder(record_string)
	

	#processed_example = some_processing(example)
	#-----------------------------------
	

	return processed_example,label

def input_pipleine(filenames,num_epochs=None):

	#create a FIFO queue for holding filenames (set capacity if needed in future)
	filename_queue = tf.train.string_input_producer([("file%d" % i) for i in range(2)]) ,shuffule=True,num_epochs=1000)

	#consume filenames 
	#done by a reader 

	#produce examples
	#call the pre-processing function here(decodes and cleans ups)
	read_dataset(filename_queue)


	#create an example queue  


def run_training():

	batch_size = 100

	#define placeholder for input 
	X = tf.placeholder(tf.float32,shape=(batch_size,1))
	Y = tf.placeholder(tf.float32,shape=(batch_size,1))

	#Define variables to be learned 


	

	# Create the graph, etc.
	init_op = tf.initialize_all_variables()

	# Create a session for running operations in the Graph.
	sess = tf.Session()

	# Initialize the variables (like the epoch counter).
	sess.run(init_op)

	# Start input enqueue threads.
	coord = tf.train.Coordinator()
	threads = tf.train.start_queue_runners(sess=sess, coord=coord)

	try:
    	while not coord.should_stop():
        # Run training steps or whatever
        sess.run(train_op)

	except tf.errors.OutOfRangeError:
    	print('Done training -- epoch limit reached')
	
	finally:
    # When done, ask the threads to stop.
    coord.request_stop()

# Wait for threads to finish.
coord.join(threads)
sess.close()

# Wait for threads to finish.
coord.join(threads)
sess.close()



def main(_):
	run_training()


if __name__ == '__main__':
  tf.app.run()