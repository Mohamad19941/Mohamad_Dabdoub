import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class LogisticRegression:
    def __init__(self, learning_rate=0.95):
        self.learning_rate = learning_rate
        self.w = None
        self.b = None
        self.losses = []

    def sigmoid(self, z):
        return 1.0 / (1 + np.exp(-z))

    def loss(self, y, y_hat):
        loss = -np.mean(y * (np.log(y_hat)) - (1 - y) * np.log(1 - y_hat))
        return loss

    def gradients(self, X, y, y_hat):
        m = X.shape[0]
        dw = (1 / m) * np.dot(X.T, (y_hat - y))
        db = (1 / m) * np.sum((y_hat - y))
        return dw, db

    def normalize(self, X):
        m, n = X.shape
        for i in range(n):
            X = (X - X.mean(axis=0)) / X.std(axis=0)
        return X

    def train(self, X, y, bs, epochs):
        X = np.array(X)
        y = np.array(y)
        m, n = X.shape
        self.w = np.zeros((n, 1))
        self.b = 0
        y = y.reshape(m, 1)
        x = self.normalize(X)

        for epoch in range(epochs):
            for i in range((m - 1) // bs + 1):
                start_i = i * bs
                end_i = start_i + bs
                xb = x[start_i:end_i]
                yb = y[start_i:end_i]
                y_hat = self.sigmoid(np.dot(xb, self.w) + self.b)
                dw, db = self.gradients(xb, yb, y_hat)
                self.w -= self.learning_rate * dw
                self.b -= self.learning_rate * db
            l = self.loss(yb, self.sigmoid(np.dot(xb, self.w) + self.b))
            self.losses.append(l)

    def plot_decision_boundary(self, df1, df2, X):
        X = np.array(X)
        x1 = [min(X[:, 0]), max(X[:, 0])]
        x_c = [-min(X[:, 0]), -max(X[:, 0])]
        m = -self.w[0] / self.w[1]
        c = -self.b / self.w[1]
        x2 = m * np.array(x1) + c
        x_0 = [x2[1], x2[0]]

        fig = plt.figure(figsize=(10, 8))
        plt.scatter(df1['X1'], df1['X2'], marker="*")
        plt.scatter(df2['X1'], df2['X2'], marker="v")
        plt.plot(x_c, x_0, 'y-')
        plt.show()

    def test(self, X_test, y_test):
        X_test = np.array(X_test)
        y_test = np.array(y_test)
        m = X_test.shape[0]
        x_test = self.normalize(X_test)
        y_pred = np.round(self.sigmoid(np.dot(x_test, self.w) + self.b))
        accuracy = np.sum(y_pred == y_test.reshape(-1, 1)) / m
        return accuracy

if __name__ == "__main__":
    data = pd.read_csv('Logistic.csv')
    data.columns = ['X1', 'X2', 'Y']
    mask = data['Y'] >= 1
    df1 = data[mask]
    df2 = data[~mask]

    logistic_model = LogisticRegression()
    logistic_model.train(data.loc[:, ['X1', 'X2']], data.loc[:, 'Y'], bs=100, epochs=100000)
    logistic_model.plot_decision_boundary(df1, df2, -data.loc[:, ['X1', 'X2']])

    X_test = data.loc[:, ['X1', 'X2']].values
    y_test = data.loc[:, 'Y'].values
    accuracy = logistic_model.test(X_test, y_test)
    print("Test Accuracy:", accuracy)
