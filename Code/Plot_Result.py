import matplotlib.pyplot as plt


def plot(x_values, y_values, labels, x_label, y_label, title):
    for i in range(len(x_values)):
        plt.plot(x_values[i], y_values[i], label=labels[i])

    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.legend()
    plt.show()

def logplot(x_values, y_values, labels, x_label, y_label, title):
    for i in range(len(x_values)):
        plt.semilogy(x_values[i], y_values[i], label=labels[i])

    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.legend()
    plt.show()