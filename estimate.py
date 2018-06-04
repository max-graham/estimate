import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple


Task = namedtuple("Task", ['min', 'likely', 'max'])


def pert(min, likely, max, scale=4.0):
    """
    Create a function that will sample from a Program and Evaluation
    Review Technique (PERT) distribution, with the given parameters
    :param min: minimum estimate
    :param likely: most likely estimate
    :param max: worst-case estimate
    :param scale: lambda factor, 4.0 is approximately normal, lower will
                  flatten and higher will sharpen the peak
    :return: a function that will generate samples from the specified
             PERT distribution
    """
    mu = (min + (scale * likely) + max) / (scale + 2)
    if mu == likely:
        # Avoid divide-by-zero problems by setting a default alpha
        a = (scale / 2) + 1
    else:
        a = ((mu - min) * (2 * likely - min - max)) / ((likely - mu) * (max - min))
    b = (a * (max - mu)) / (mu - min)

    def pert_pdf_sampler(num_samples):
        return np.random.beta(a=a, b=b, size=num_samples) * (max - min) + min
    return pert_pdf_sampler


def mc_estimate(num_samples, tasks):
    """
    Runs a Monte Carlo simulation in order to generate probabilistic effort estimates for a set of tasks.

    Returns a numpy.array of simulation results, which represent the total time required to complete all tasks.
    Values are sampled from a beta-PELT distribution for each task, defined by the min, max, and most likely
    values defined for each task. Those sampled times are then aggregated to give a probabilistic estimate of the
    total time to complete all listed tasks.

    :param num_samples: int, the number of simulations to run for the Monte Carlo simulation
    :param tasks: list of 3-tuples with shape (min_estimate, most_likely, max_estimate), or the Task named tuple
    :return: np.array with shape (num_samples,), representing the total time required to complete
            the tasks for a given simulation run.
    """
    task_sims = []
    for task in tasks:
        pdf = pert(min=task.min, likely=task.likely, max=task.max)
        samples = pdf(num_samples).reshape((-1, 1))
        task_sims.append(samples)
    sims = np.concatenate(task_sims, axis=1)
    return sims.sum(axis=1)


def generate_plots(sims, bins, filepath):
    """
    Given a set of simulated estimates, generate the PDF and CDF graphs with 50%, 90%, 95%, and 99%
    confidence indicators.

    Estimates are expected to come from the mc_estimate function.

    :param sims: np.array of simulation results
    :param bins: number of bins to use in each histogram
    :param filepath: path where you want to save the plot
    :return: None; generates a plot and saves it to disk
    """
    fig, axarr = plt.subplots(2, figsize=(16, 9))

    # TODO(Max): Make confidence indicators configurable
    sims = np.sort(sims)
    num_sims = sims.shape[0]
    conf_50 = sims[int(num_sims * 0.5)]
    conf_90 = sims[int(num_sims * 0.9)]
    conf_95 = sims[int(num_sims * 0.95)]
    conf_99 = sims[int(num_sims * 0.99)]

    # PDF
    axarr[0].hist(sims, bins=bins, cumulative=False, normed=False)
    axarr[0].set(title='Monte Carlo Simulation Results ({} runs)'.format(num_sims), ylabel='Number of Simulations')

    # CDF
    axarr[1].hist(sims, bins=bins, cumulative=True, normed=True)
    axarr[1].set(xlabel='Hours', ylabel='Cumulative Density')

    # Confidence indicators
    for ax in axarr:
        ax.axvline(x=conf_50, color='k', linestyle='--', label="50% quantile: {}".format(round(conf_50)))
        ax.axvline(x=conf_90, color='r', linestyle=':', label="90% quantile: {}".format(round(conf_90)))
        ax.axvline(x=conf_95, color='r', linestyle='--', label="95% quantile: {}".format(round(conf_95)))
        ax.axvline(x=conf_99, color='r', label="99% quantile: {}".format(round(conf_99)))

    plt.legend()
    plt.savefig(fname=filepath)


def main():
    mc_simulations = 100000
    plot_path = '/home/max/Desktop/estimate.png'

    # Each tuple should be (min, likely, max) effort estimates for the tasks
    # e.g. Task(min=1, likely=4, max=12)

    task_list = [
       # tasks here
       Task(min=1, likely=4, max=12),
    ]

    sims = mc_estimate(num_samples=mc_simulations, tasks=task_list)
    generate_plots(sims, bins=50, filepath=plot_path)


if __name__ == "__main__":
    main()
