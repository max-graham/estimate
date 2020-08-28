import numpy as np


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
        a = ((mu - min) * (2 * likely - min - max)) / ((likely - mu) *
                                                       (max - min))
    b = (a * (max - mu)) / (mu - min)

    def pert_pdf_sampler(num_samples):
        return np.random.beta(a=a, b=b, size=num_samples) * (max - min) + min

    return pert_pdf_sampler


def monte_carlo(num_samples, tasks):
    """
    Runs a Monte Carlo simulation in order to generate probabilistic effort
    estimates for a set of tasks.

    Returns a numpy.array of simulation results, which represent the total time
    required to complete all tasks. Values are sampled from a beta-PELT
    distribution for each task, defined by the min, max, and most likely values
    defined for each task. Those sampled times are then aggregated to give a
    probabilistic estimate of the total time to complete all listed tasks.

    :param num_samples: int, the number of simulations to run for the Monte
                        Carlo simulation
    :param tasks: list of 3-tuples with shape
                (min_estimate, most_likely, max_estimate)
    :return: np.array with shape (num_samples,), representing the total time
            required to complete the tasks for a given simulation run.
    """
    task_sims = []
    for task in tasks:
        pdf = pert(min=task.min, likely=task.likely, max=task.max)
        samples = pdf(num_samples).reshape((-1, 1))
        task_sims.append(samples)
    sims = np.concatenate(task_sims, axis=1)
    return sims.sum(axis=1)
