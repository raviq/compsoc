#
import os
import importlib
import pandas as pd
import matplotlib.pylab as plt
import numpy as np


def plot_final_results(name, results, num_voters, num_candidates, num_topn, number_iterations):
    """
    Plot the mean scores for all voting rules
    name : str
        The name of voters model
    results : dict
        results of the simulation. Key is index of iteration.
    """
    # Aggregate results
    voting_rules = list(results[0].keys())
    results_agg = []
    for rule in voting_rules:
        for i in range(number_iterations):
            r = results[i][rule]
            r['rule'] = rule
            results_agg.append(r)
    df = pd.DataFrame(results_agg)
    df = df.set_index('rule')
    # Summarize the results using pivot_table
    df_summary = df.pivot_table(values=['top', 'topn'],
                                index=df.index.get_level_values(0),
                                aggfunc={'top': ['mean', 'std'],
                                         'topn': ['mean', 'std']})
    df_summary.columns = df_summary.columns.map('_'.join)
    # Plot the scores for all voting rules
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.subplots_adjust(bottom=0.25)
    df_summary.plot(y="top_mean", yerr="top_std", legend=False,
                    capsize=2, fmt='o-', color='b',
                    rot=90, ax=axes[0])
    axes[0].set_xticks(np.arange(len(df_summary)))
    axes[0].set_xticklabels(df_summary.index)
    axes[0].set_xlabel("Voting rules")
    axes[0].set_ylabel("Mean scores")
    axes[0].set_title('Top mean')
    axes[0].grid(color='gray', linestyle='dashed', linewidth=0.1)
    df_summary.plot(y="topn_mean", yerr="topn_std", legend=False,
                    capsize=2, fmt='o-', color='g',
                    rot=90, ax=axes[1])
    axes[1].set_xticks(np.arange(len(df_summary)))
    axes[1].set_xticklabels(df_summary.index)
    axes[1].set_xlabel("Voting rules")
    axes[1].set_ylabel("Mean scores")
    axes[1].set_title('Top{} mean'.format(num_topn))
    axes[1].grid(color='gray', linestyle='dashed', linewidth=0.1)
    fig.suptitle(
        "{} voters voting for {} {}-candidates\n {} iterations".format(num_voters, num_candidates,
                                                                       name, number_iterations))
    plt.savefig(f"figures/scores_{num_candidates}_{num_voters}_{name}_{number_iterations}.png",
                format='png', dpi=500)


# int-str converters
def int_list_to_str(l):
    return ','.join(map(str, l))


def str_list_to_in(l):
    return list(map(int, l.split(",")))

# -- print (sorted(str_list_to_in('1,2,5,4,3,0,6')))
