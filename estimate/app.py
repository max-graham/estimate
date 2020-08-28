import json
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple
import click

from .simulation import monte_carlo
from .plotting import generate_plots

Task = namedtuple("Task", ['min', 'likely', 'max'])


@click.command()
@click.option('--num_sims',
              default=1000000,
              help='Number of simulations to run in the Monte Carlo')
@click.option('--infile', default='tasks.json', help='Path to tasks.json')
@click.option('--outfile',
              default='estimate.png',
              help='Path to desired output .png file')
@click.option('--units',
              default='Days',
              help='Time unit for estimates (e.g. Days, Hours, etc.)')
def task_estimation(num_sims, infile, outfile, units):
    task_list = load_tasks(infile=infile)
    sims = monte_carlo(num_samples=num_sims, tasks=task_list)
    generate_plots(sims, bins=50, time_unit=units, filepath=outfile)


def load_tasks(infile):
    with open(infile, 'r') as f:
        tasks = json.load(f)
    task_list = []
    for task in tasks:
        task_list.append(
            Task(
                min=task['min'],
                likely=task['likely'],
                max=task['max'],
            ))
    return task_list
