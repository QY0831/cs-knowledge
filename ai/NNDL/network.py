import random
import numpy as np

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z) * (1 - sigmoid(z))

class Network(object):
    def __init__(self, sizes): 
        # size 是一个整数列表，其中第 i 个整数表示第 i 层神经元的数量
        # 例如，如果列表为 [2, 3, 1]，则网络有 3 层：
        # 第一层有 2 个神经元，第二层有 3 个神经元，第三层有 1 个神经元。
        #
        # np.random.randn 从标准正态分布生成随机数
        # 它初始化网络的权重和偏差（GCD 的开始）

        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        # weights[0] -> w1 = [[w11, w12], [w21, w22], [w31, w32]]
        # wij：i表示隐藏层的第i个神经元，j表示输入层的第j个神经元
        # biases[0] -> b1 = [[b11], [b12], [b13]]
        # 假设输入向量[x1 x2]
        # z1 = w1 * x + b1 = [[w11, w12], [w21, w22], [w31, w32]] * [[x1], [x2]] + [[b11], [b12], [b13]] 
        #                  = [[w11*x1 + w12*x2 + b11], [w21*x1 + w22*x2 + b12], [w31*x1 + w32*x2 + b13]]
        # a' = sigmoid(w * a + b[1])

        
    def feedforward(self, a):
        # a: 激活向量
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a) + b)
        return a
    
    def cost_derivative(self, output_activations, y):
        return (output_activations - y)
    
    def backprop(self, x, y):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        activation = x
        activations = [x]
        zs = []
        # 前馈
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = sigmoid(z)
            activations.append(activation)
        # 反向传播
        delta = self.cost_derivative(activations[-1], y) * sigmoid_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-1]
            sp = sigmoid_prime(z)
            delta = np.dot(self.weights[-l+1].transpose(), delta) * sp
            nabla_b[-1] = delta
            nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        return (nabla_b, nabla_w)

    def update_mini_batch(self, mini_batch, eta):
        # mini_batch: 小批量数据集 (x, y) 元组的列表
        # eta: 学习率
        # 初始化累计梯度变化
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            # 计算每个小批量的梯度变化并累加
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)] 
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        # 更新权重和偏差
        # eta / len(mini_batch): 每个样本对最终梯度更新的贡献
        self.weights = [
            w - (eta / len(mini_batch)) * nw for w, nw in zip(self.weights, nabla_w)
        ]
        self.biases = [
            b - (eta / len(mini_batch)) * nb for b, nb in zip(self.biases, nabla_b)
        ]
    
    
    def SGD(self, training_data, epochs, mini_batch_size, eta, test_data=None):
        # training_data: 训练数据集 (x, y)元组的列表
        # epochs: 轮次
        # mini_batch_size: 每个小批量的大小
        # eta: 学习率
        # test_data: 测试数据集 (x, y)元组的列表
        if test_data:
            n_test = len(test_data)
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k: k+mini_batch_size] for k in range(0, n, mini_batch_size)
            ]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            if test_data:
                print(f"Epoch {j}: {self.evaluate(test_data)} / {n_test}")
            else:
                print(f"Epoch {j} complete")