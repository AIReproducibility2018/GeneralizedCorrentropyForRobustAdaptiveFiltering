import GMCC as gmcc
import numpy as np
import Plot_Result
import WriteJSON as jsonwriter


def monte_carlo_simulation(mu, llambda, alfa, generator):
    w0 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1])
    w = [0]*len(w0)
    gmcc_program = gmcc.GMCC(w0, gmcc.Type_Of_Distribution.standard, alfa, llambda, mu, 0.0, 1.0, 0.0, 1.0, generator)

    for i in range(1000):
        w = gmcc_program.iterate()

    pod = np.power(np.linalg.norm( w0 - w ), 2)
    run = {'POD': pod, 'Weights':np.ndarray.tolist(w)}
    return run

def has_other_than_zero(a):
    for v in a:
        if v != 0:
            return True
    return False

def simulations(mu, llambda, alfa, generator, writer):
    sum = 0.0
    divergent = 0.0
    number_of_runs = 1000
    runs = []
    for i in range(number_of_runs):
        run = monte_carlo_simulation(mu, llambda, alfa, generator)
        div = run['POD']
        runs.append(run)
        sum += div
        if div > 100:
            divergent += 1.0
    avg = sum / number_of_runs
    div_percent = divergent / number_of_runs
    data = {'Hyperparameters':{'Mu':mu, 'Lambda':llambda, 'Alfa':alfa}, 'Runs':runs}
    writer.add_object(data)
    step_size = mu * llambda * alfa
    # print(str(step_size)+';'+str(div_percent))
    #print('Step_size: '+str(step_size)+'\tAvg: '+str(avg)+'\tDivergent Rate: '+str(div_percent) + '\tTotal Divergent: '+str(divergent))
    return [step_size, div_percent]


def pod_simulation(should_save_json = False):
    generator = np.random
    generator.seed(0)
    writer = jsonwriter.WriteJSON(should_save_json)
    max_step_size = 0.3
    alfa = 4.0
    llambda = 0.03
    min_mu = 0.0
    max_mu = max_step_size / (alfa * llambda)
    number_of_iterations = 32
    mu_step = (max_mu - min_mu) / number_of_iterations
    x_values = []
    y_values = []
    for i in range(number_of_iterations+1):
        mu = min_mu + mu_step * i
        r = simulations(mu, llambda, alfa, generator, writer)
        x_values.append(r[0])
        y_values.append(r[1])

    writer.save_json('POD')

    Plot_Result.plot([x_values], [y_values], ['GMCC'], 'Step Size', 'POD', 'POD' )

pod_simulation()
