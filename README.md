
## About: 

The allocation of resources to process tasks can have a significant impact on the performance (such as cost, time) of those tasks, and hence of the overall process. Past resource allocation decisions, when correlated with process execution histories annotated with quality of service (or performance) measures, can be a rich source of knowledge about the best resource allocation decisions. The optimality of resource allocation decisions is not determined by the process instance alone, but also by the context in which these instances are executed. This phenomenon turns out to be even more compelling when the resources in question are human resources. Human workers with same the organizational role and capabilities can have heterogeneous behaviors based on their operational context. In this work, we propose an approach to supporting resource allocation decisions by extracting information about the process context and process performance from past process executions. 

| DataSet                              | Configuration | Epochs | Train   | Valid   | Test    |
| ------------------------------------ | ------------- | ------ | ------- | ------- | ------- |
| ResourceWithAmountContext            | Medium        | 13     | 74.045  | 187.323 | 191.933 |
| ResourceWithOUtContext               | Medium        | 13     | 2.050   | 2.321   | 2.518   |
| ResourceWithWL&AmountContext         | Medium        | 13     | 77.944  | 161.044 | 164.025 |
| ResourceWithAmountFamiliarityContext | Medium        | 13     | 404.591 | 498.988 | 517.228 |
| ResourceWithAmountContext            | Large         | 25     | 51.332  | 151.331 | 149.891 |
| ResourceWithOUtContext               | Large         | 25     | 2.050   | 2.271   | 2.518   |
| ResourceWithWL&AmountContext         | Large         | 25     | 48.452  | 135.032 | 137.056 |
| ResourceWithAmountFamiliarityContext | Large         | 25     | 159.232 | 372.712 | 371.158 |




## Results: 


We trained LSTM network of two sizes with configuration labelled as medium and large in Table above.  Both Networks have two layers and unrolled it has 35 steps. At its core the model consists of an LSTM cell that processes one task(executed by a particular resource) at a time and the network computes probability values for the next task in the sequence. The network memory state is initialized using a vector of zeros.  The network updates itself after reading each task in the given the sequence. Because of computational resource constraints we processed the data in mini-batches of size 20. The medium LSTM network has 200 units per layer and its parameters are initialized uniformly in [−0.1, 0.1]. The medium model was trained for 13 epochs with a learning rate of 1.0 and after 4 epochs we reduce the learning rate by a factor of 0.8 after each epoch. The large LSTM network has 650 units per layer and we initialize its parameters uniformly in [-0.05,0.05].  We train the LSTM for 25 epochs with a learning rate of 1.0, and after 6 epochs we decrease it by a factor of 1/1.15 after each epoch. We clip the norm gradients of both network (normalized by minibatch size) at 5. Training this network takes about one and a half hour on an 2.4GHz Macbook Pro.   
