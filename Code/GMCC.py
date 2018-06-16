import numpy as np
import enum
import math

class GMCC:

    def __init__(self, w0, type_of_noise, alfa, llambda, mu, input_mean, input_variance, noise_mean, noise_variance, generator):

        self.generator = generator
        self.filter_length = len(w0)
        self.w0 = w0
        self.type_of_noise = type_of_noise
        self.w = np.zeros(self.filter_length)
        self.alfa = alfa
        self.llambda = llambda
        self.mu = mu
        self.eta = mu * llambda * alfa
        self.input_mean = input_mean
        self.input_variance = input_variance
        self.noise_mean = noise_mean
        self.noise_variance = noise_variance
        self.x = None
        self.v = None

    def gaussian(self, mean, variance):
        return self.generator.normal(mean, variance, self.filter_length)

    def calculate_w(self, d):
        wtx = np.transpose(self.w) * self.x
        e = d - wtx
        return self.w + self.eta * np.exp(-self.llambda * np.power(np.abs(e), self.alfa)) * np.power(np.abs(e), self.alfa - 1) * np.sign(e) * self.x

    def get_d(self):
        self.calculate_noise()
        self.x = self.gaussian(self.input_mean, self.input_variance)
        d = np.transpose(self.w0) * self.x + self.v
        return d

    def calculate_distribution(self, p, low, high):
        a = []
        for i in range(self.filter_length):
            if self.generator.uniform(0, 1.0) < p:
                a.append(high)
            else:
                a.append(low)
        return np.array(a)

    def calculate_noise(self):
        if self.type_of_noise == Type_Of_Distribution.standard:
            self.v = self.gaussian(self.noise_mean, self.noise_variance)
        else:
            a = self.calculate_distribution(0.06, 0.0, 1.0)
            B = self.generator.normal(0.0, 15.0, self.filter_length)
            A = None
            if self.type_of_noise == Type_Of_Distribution.Gaussian:
                A = self.generator.normal(0.0, 1.0, self.filter_length)
            elif self.type_of_noise == Type_Of_Distribution.Binary:
                A = self.calculate_distribution(0.5, -1.0, 1.0)
            elif self.type_of_noise == Type_Of_Distribution.Laplace:
                A = self.generator.laplace(0.0, 1.0, self.filter_length)
            elif self.type_of_noise == Type_Of_Distribution.Uniform:
                A = self.generator.uniform(-math.sqrt(3.0), math.sqrt(3.0))
            self.v = (1-a) * A + a * B

    def iterate(self):
        d = self.get_d()
        self.w = self.calculate_w(d)
        return self.w


class Type_Of_Distribution(enum.Enum):
    standard = 0,
    Gaussian = 1,
    Binary = 2,
    Laplace = 3,
    Uniform = 4
