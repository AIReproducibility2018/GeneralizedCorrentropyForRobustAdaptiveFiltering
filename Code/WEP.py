import GMCC as gmcc
import numpy as np
import WriteJSON as jsonwriter


import GMCC as gmcc
import numpy as np
import Plot_Result


def monte_carlo_simulation(mu, llambda, alfa, type_of_distribution, generator):
    w0 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1])
    gmcc_program = gmcc.GMCC(w0, type_of_distribution, alfa, llambda, mu, 0.0, 1.0, 0.0, 1.0, generator)
    y_values = []
    x_values = []
    # steps = []
    for i in range(10000):
        w = gmcc_program.iterate()
        wep = np.power(np.linalg.norm( w0 - w ), 2)
        y_values.append(wep)
        # step = {'Iteration':i, 'Weight Error Power': wep, 'Weights': np.ndarray.tolist(w)}
        # steps.append(step)
        x_values.append(i)
    return [x_values, y_values]

def monte_carlo_simulations(mu, llambda, alfa, type_of_distribution, generator, writer):
    y_total_values = [0]*10000
    x_values = []
    number_of_runs = 100
    # runs = []
    for i in range(number_of_runs):
        x_values, y_values = monte_carlo_simulation(mu, llambda, alfa, type_of_distribution, generator)
        # runs.append(steps)
        for j in range(len(y_values)):
            y_total_values[j] += y_values[j]
    # writer.add_object(runs)
    y_values = [y/float(number_of_runs) for y in y_total_values]
    # data = {'Hyperparameters':{'Mu':mu, 'Lambda':llambda, 'Alfa':alfa},'Weight Error Power Values':y_values, 'Runs':runs}
    data = {'Hyperparameters': {'Mu': mu, 'Lambda': llambda, 'Alfa': alfa}, 'Weight Error Power Values': y_values}
    writer.add_object(data)
    return [x_values, y_values]

def wep_simulation(desired_type_of_distribution, should_save_json = False):
    running_parameters = [
        [
            gmcc.Type_Of_Distribution.Gaussian,
            [
                [1.0, 0.01, 0.003, 'Alfa=1, Lambda=0.01, Mu=0.003'],
                [2.0, 0.1, 0.003,  'Alfa=2, Lambda=0.1,  Mu=0.003'],
                [4.0, 0.03, 0.0013, 'Alfa=4, Lambda=0.03, Mu=0.0013'],
                [6.0, 0.01, 0.00055, 'Alfa=6, Lambda=0.01, Mu=0.00055']
            ]
        ],
        [
            gmcc.Type_Of_Distribution.Binary,
            [
                [1.0, 0.01, 0.0045, 'Alfa=1, Lambda=0.01, Mu=0.0045'],
                [2.0, 0.05, 0.0035, 'Alfa=2, Lambda=0.05,  Mu=0.0035'],
                [4.0, 0.03, 0.0012, 'Alfa=4, Lambda=0.03, Mu=0.0012'],
                [6.0, 0.01, 0.0005, 'Alfa=6, Lambda=0.01, Mu=0.0005']
            ]
        ],
        [
            gmcc.Type_Of_Distribution.Laplace,
            [
                [1.0, 0.01, 0.0035, 'Alfa=1, Lambda=0.01, Mu=0.0035'],
                [2.0, 0.05, 0.0035, 'Alfa=2, Lambda=0.05,  Mu=0.0035'],
                [4.0, 0.03, 0.0023, 'Alfa=4, Lambda=0.03, Mu=0.0023'],
                [6.0, 0.01, 0.0009, 'Alfa=6, Lambda=0.01, Mu=0.0009']
            ]
        ],
        [
            gmcc.Type_Of_Distribution.Uniform,
            [
                [1.0, 0.01, 0.004, 'Alfa=1, Lambda=0.01, Mu=0.004'],
                [2.0, 0.1, 0.0034, 'Alfa=2, Lambda=0.1,  Mu=0.0034'],
                [4.0, 0.03, 0.0013, 'Alfa=4, Lambda=0.03, Mu=0.0013'],
                [6.0, 0.01, 0.0005, 'Alfa=6, Lambda=0.01, Mu=0.0005']
            ]
        ]
    ]

    writer = jsonwriter.WriteJSON(should_save_json)

    x_list = []
    y_list = []
    labels = []

    generator = np.random
    generator.seed(0)

    for i in range(len(running_parameters)):
        type_of_distribution = running_parameters[i][0]
        hyperparameters = running_parameters[i][1]

        if type_of_distribution != desired_type_of_distribution:
            continue

        for j in range(len(hyperparameters)):
            alfa = hyperparameters[j][0]
            llambda = hyperparameters[j][1]
            mu = hyperparameters[j][2]

            x_values, y_values = monte_carlo_simulations(mu, llambda, alfa, type_of_distribution, generator, writer)
            labels.append(hyperparameters[j][3])
            x_list.append(x_values)
            y_list.append(y_values)
        writer.save_json(type_of_distribution.name)
        plot_title = type_of_distribution.name + ' Distribution'
        Plot_Result.logplot(x_list, y_list, labels, 'Iteration', 'Weight Error Power', plot_title)

wep_simulation(gmcc.Type_Of_Distribution.Uniform)
