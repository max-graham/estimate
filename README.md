# Estimate
Project-level estimation using Monte Carlo task simulation

Uses the PERT methodology to generate a probability distribution of the time to complete each task,
based on a best-case, most-likely, and worst-case estimate supplied from the user.

Each task's probability distribution is sampled N times and summed across a run (one sample for each task)
to generate an overall estimate for the time to complete all tasks. The 50%, 90%, 95%, and 99% percentiles
are calculated and graphed to inform the user of the overall effort required to complete the work.
