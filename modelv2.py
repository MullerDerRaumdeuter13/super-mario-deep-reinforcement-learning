import tensorflow as tf
import numpy as np
import random

class DQNetwork:
    def __init__(self, state_size, action_size, learning_rate, name='DQNetwork'):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        
        with tf.compat.v1.variable_scope(name):
            # we create placeholders
            self.inputs_ = tf.compat.v1.placeholder(tf.float32, [None, *state_size], name="inputs") 
            self.actions_ = tf.compat.v1.placeholder(tf.float32, [None, self.action_size], name="actions_")
            
            # remember that target_Q is the R(s,a) + ymax Qhats(s', a')            
            self.target_Q = tf.compat.v1.placeholder(tf.float32, [None], name="target")
            
            # input is 100x128x4
            self.conv1 = tf.compat.v1.layers.conv2d(inputs=self.inputs_, 
                             filters=32,
                             kernel_size=[8,8],
                             strides=[4,4],
                             padding="VALID",
                             kernel_initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"),
                             name="conv1")
            self.conv1_out = tf.nn.elu(self.conv1, name="conv1_out")
            
            self.conv2 = tf.compat.v1.layers.conv2d(inputs=self.conv1_out, 
                             filters=64,
                             kernel_size=[4,4],
                             strides=[2,2],
                             padding="VALID",
                             kernel_initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"),
                             name="conv2")
            self.conv2_out = tf.nn.elu(self.conv2, name="conv2_out")
            
            self.conv3 = tf.compat.v1.layers.conv2d(inputs=self.conv2_out, 
                             filters=32,
                             kernel_size=[3,3],
                             strides=[2,2],
                             padding="VALID",
                             kernel_initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"),
                             name="conv3")
            self.conv3_out = tf.nn.elu(self.conv3, name="conv3_out")
            
            self.flatten = tf.contrib.layers.flatten(self.conv3_out)
            
            self.fc = tf.compat.v1.layers.dense(inputs=self.flatten,
                             units=512,
                             activation=tf.nn.elu,
                             kernel_initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"),
                             name="fc1")
            
            self.output = tf.compat.v1.layers.dense(inputs=self.fc,
                             units=self.action_size,
                             activation=None,
                             kernel_initializer=tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform"))
            
            # Q is our predicted Q value
            self.Q = tf.reduce_sum(input_tensor=tf.multiply(self.output, self.actions_))
            
            # the loss is the difference between our predicted Q_values and the Q_target
            # sum(Q_target - Q)^2
            self.loss = tf.reduce_mean(input_tensor=tf.square(self.target_Q - self.Q))
            
            self.optimizer = tf.compat.v1.train.AdamOptimizer(self.learning_rate).minimize(self.loss)