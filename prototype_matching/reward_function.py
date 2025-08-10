import numpy as np
import matplotlib.pyplot as plt

def reward(mu, nu):
    nu = np.clip(np.sqrt(nu) * 1.75, 0.0, 1.0)
    return ((mu+1)*nu - 1) # *np.abs(mu)

if __name__ == "__main__":
    print("mu=1, nu=1, reward=", reward(1, 1))
    print("mu=-1, nu=0, reward=", reward(-1, 0))
    print("mu=1, nu=0, reward=", reward(1, 0))
    print("mu=-1, nu=1, reward=", reward(-1, 1))


    mu = np.linspace(-1, 1, 100)
    nu = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(mu, nu)
    Z = reward(X, Y)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z)
    plt.xlabel("mu")
    plt.ylabel("nu")
    # plt.show()


    X = nu
    plt.figure(figsize=(10, 3))

    Z = reward(-1, X)
    plt.subplot(131)
    plt.ylim(-1.05, 1.05)
    plt.plot(X, Z)
    plt.xlabel("nu")
    plt.title("mu=-1")

    Z = reward(0, X)
    plt.subplot(132)
    plt.ylim(-1.05, 1.05)
    plt.plot(X, Z)
    plt.xlabel("nu")
    plt.title("mu=0")

    Z = reward(1, X)
    plt.subplot(133)
    plt.ylim(-1.05, 1.05)
    plt.plot(X, Z)
    plt.xlabel("nu")
    plt.title("mu=1")



    plt.show()


