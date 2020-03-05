"""
Plot result function
"""

import matplotlib.pyplot as plt


def plot_results(scoreArray, game_index_array, weights):
    # initializing the plot figure
    def __init_plot():
        plt.figure(1)
        plt.subplot(211)
        plt.plot(game_index_array, scoreArray, 'k-')
        plt.xlabel('Game Number')
        plt.ylabel('Game Score')
        plt.title('Learning Curve')
        plt.xlim(1, max(game_index_array))
        plt.ylim(0, max(scoreArray) * 1.1)

    # define function per number of weights
    def plot_result_0():
        __init_plot()
        plt.show()

    def plot_result_1(label_0):
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        plt.title('Learning Curve')
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label=label_0)
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    def plot_result_2(label_0, label_1):
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        plt.title('Learning Curve')
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label=label_0)
        plt.plot(game_index_array, weights[1], label=label_1)
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    def plot_result_3(label_0, label_1, label_2):
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        plt.title('Learning Curve')
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label=label_0)
        plt.plot(game_index_array, weights[1], label=label_1)
        plt.plot(game_index_array, weights[2], label=label_2)
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    def plot_result_4(label_0, label_1, label_2, label_3):
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        plt.title('Learning Curve')
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label=label_0)
        plt.plot(game_index_array, weights[1], label=label_1)
        plt.plot(game_index_array, weights[2], label=label_2)
        plt.plot(game_index_array, weights[3], label=label_3)
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    # chosing which plot function will be returned
    if len(weights) == 0:
        return plot_result_0
    elif len(weights) == 1:
        return plot_result_1
    elif len(weights) == 2:
        return plot_result_2
    elif len(weights) == 3:
        return plot_result_3
    elif len(weights) == 4:
        return plot_result_4
    else:
        return lambda: print("Too much weights!")

# def plot_results(scoreArray, game_index_array, w0, w1, w2, w3):
#     plt.figure(1)
#     plt.subplot(211)
#     plt.plot(game_index_array, scoreArray, 'k-')
#     plt.xlabel('Game Number')
#     plt.ylabel('Game Score')
#     plt.title('Learning Curve')
#     plt.xlim(1, max(game_index_array))
#     plt.ylim(0, max(scoreArray) * 1.1)

#     # Plot the weights over time
#     plt.subplot(212)
#     plt.xlabel('Game Number')
#     plt.ylabel('Weights')
#     plt.title('Learning Curve')
#     ax = plt.gca()
#     ax.set_yscale('log')
#     plt.plot(game_index_array, w0, label="Aggregate Height")
#     plt.plot(game_index_array, w1, label="Unevenness")
#     plt.plot(game_index_array, w2, label="Maximum Height")
#     plt.plot(game_index_array, w3, label="Number of Holes")
#     plt.legend(loc='lower left')
#     plt.xlim(0, max(game_index_array))
#     plt.ylim(0.0001, 100)
#     plt.show()

# def plot_results(scoreArray, game_index_array):
#     plt.figure(1)
#     plt.subplot(211)
#     plt.plot(game_index_array, scoreArray, 'k-')
#     plt.xlabel('Game Number')
#     plt.ylabel('Game Score')
#     plt.title('Learning Curve')
#     plt.xlim(1, max(game_index_array))
#     plt.ylim(0, max(scoreArray) * 1.1)
#     plt.show()