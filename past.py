import tensorflow as tf

# Check for GPU availability
if tf.test.is_gpu_available():
    print("GPU is available 🚀")
    # TensorFlow will automatically use the GPU for computations
    # Your neural network code goes here
else:
    print("No GPU found 😔")
    # Your code will run on the CPU
