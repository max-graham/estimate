import numpy as np
import matplotlib.pyplot as plt


def generate_plots(sims, bins, time_unit, filepath):
    """
    Given a set of simulated estimates, generate the PDF and CDF graphs with
    50%, 90%, 95%, and 99% confidence indicators.

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
    axarr[0].hist(sims, bins=bins, cumulative=False, density=False)
    axarr[0].set(
        title='Monte Carlo Simulation Results ({} runs)'.format(num_sims),
        ylabel='Number of Simulations')

    # CDF
    axarr[1].hist(sims, bins=bins, cumulative=True, density=True)
    axarr[1].set(xlabel=time_unit,
                 ylabel=f'Probability of Finishing within X {time_unit}')

    # Confidence indicators
    for ax in axarr:
        ax.axvline(x=conf_50,
                   color='k',
                   linestyle='--',
                   label="50% prob. of finishing: {n} {units}".format(
                       n=int(conf_50), units=time_unit))
        ax.axvline(x=conf_90,
                   color='r',
                   linestyle=':',
                   label="90% prob. of finishing: {n} {units}".format(
                       n=int(conf_90), units=time_unit))
        ax.axvline(x=conf_95,
                   color='r',
                   linestyle='--',
                   label="95% prob. of finishing: {n} {units}".format(
                       n=int(conf_95), units=time_unit))
        ax.axvline(x=conf_99,
                   color='r',
                   label="99% prob. of finishing: {n} {units}".format(
                       n=int(conf_99), units=time_unit))

    plt.legend()
    plt.savefig(fname=filepath)
