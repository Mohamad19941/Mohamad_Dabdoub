import numpy as np
import matplotlib.pyplot as plt

class QuadraticRegression:
    def __init__(self, learning_rate=1.2, max_iter=100000):
        self.learning_rate = learning_rate
        self.max_iter = max_iter
        self.theta = [1, 1, 1]

    def h(self, X):
        X2 = np.square(X)
        return self.theta[0] + self.theta[1] * X + self.theta[2] * X2

    def J(self, X, Y):
        m = len(X)
        c = self.h(X) - Y
        return np.sum((1 / (2 * m)) * c * np.transpose(c))

    def gradient_descent(self, X, Y):
        m = len(X)
        X0 = np.ones(m)
        X2 = np.square(X)
        XX = np.array([X0, X, X2])
        for _ in range(self.max_iter):
            d = (1 / m) * np.dot((self.h(X) - Y), XX.T)
            self.theta -= self.learning_rate * d
        return self.theta

    def fit(self, X, Y):
        self.theta = self.gradient_descent(X, Y)

    def plot(self, X, Y):
        plt.scatter(X, Y)
        WW = [self.theta[0] + self.theta[1] * x + self.theta[2] * x ** 2 for x in X]
        plt.plot(X, WW)
        plt.show()

# Example usage
if __name__ == "__main__":
    X = [1.5, 2.25, 2.3, 2.475, 3.7, 5, 6.5, 6.7, 7.7, 10, 11.2]
    X = np.array(X) / max(X)
    Y = [0.01928584, 0.05, 0.051, 0.056, 0.125, 0.2125, 0.37, 0.39, 0.51, 0.65, 1]
    qr = QuadraticRegression()
    qr.fit(X, Y)
    qr.plot(X, Y)
