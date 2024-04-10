import numpy as np
import matplotlib.pyplot as plt

class LinearRegression:
  def __init__(self, learning_rate=0.1, max_iter=1000):
    self.learning_rate = learning_rate
    self.max_iter = max_iter
    self.theta = None  # Initialize theta as None

  def fit(self, X, Y):
    X = np.array(X)
    Y = np.array(Y)
    m = len(X)

    self.theta = np.zeros(2)

    J_cost = []
    for i in range(self.max_iter):
      # Calculate derivatives
      derivative = sum((1/m)*(self.predict(X) - Y))
      derivative1 = sum((1 / m) * (self.predict(X) - Y)*X)

      # Update theta
      self.theta[0] -= self.learning_rate * derivative
      self.theta[1] -= self.learning_rate * derivative1

      # Calculate cost
      J_cost.append(self.cost(X, Y))

    # Plot results
    WW = []
    for ii in range(len(X)):
      WW.append(self.theta[0] + self.theta[1]*X[ii])
    plt.scatter(X, Y)
    plt.plot(X, WW)
    plt.show()

  def predict(self, X):
    X = np.array(X)
    return self.theta[0] + X * self.theta[1]

  def cost(self, X, Y):
    Y = np.array(Y)
    m = len(X)
    return sum((1/(2*m)) * (self.predict(X) - Y)**2)

# Example usage
model = LinearRegression()
model.fit(X, Y)
predictions = model.predict([0.25])  # Predict for a new feature value
print(predictions)
