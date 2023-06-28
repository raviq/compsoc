"""
Plot
"""
import numpy as np
import pandas as pd
from matplotlib import pylab as plt
from matplotlib import use
from base64 import b64encode
from io import BytesIO

use("Agg")  # Use non-interactive backend for mpl


def plot_comparison_results(voter_model: str, results: dict, num_voters: int, num_candidates: int,
                            num_topn: int,
                            number_iterations: int, distort_rate = 0.0 , save_figure: bool = False):
    """
    Plot the mean scores for all voting rules.

    :param voter_model: The generative model to use.
    :type voter_model: str
    :param results: The voting rule result data to be plotted. Key is index of iteration.
    :type results: dict
    :param num_voters: The number of voters in the model.
    :type num_voters: int
    :param num_candidates: The number of candidates in the model.
    :type num_candidates: int
    :param num_topn: The number of top candidates to consider.
    :type num_topn: int
    :param number_iterations: The number of iterations for the simulation.
    :type number_iterations: int
    :param save_figure: If True, saves the figure as a png file, defaults to False.
    :type save_figure: bool, optional
    :return: Base64 encoded string representation of the plot image.
    :rtype: str
    """
    # Aggregate results
    voting_rules = list(results[0].keys())
    results_agg = []
    for rule in voting_rules:
        for i in range(number_iterations):
            r = results[i][rule]
            r["rule"] = rule
            results_agg.append(r)
    df = pd.DataFrame(results_agg)
    df = df.set_index("rule")
    # Summarize the results using pivot_table
    df_summary = df.pivot_table(values=["top", "topn"],
                                index=df.index.get_level_values(0),
                                aggfunc={"top": ["mean", "std"],
                                         "topn": ["mean", "std"]})
    df_summary.columns = df_summary.columns.map("_".join)
    # Plot the scores for all voting rules
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.subplots_adjust(bottom=0.25)
    df_summary.plot(y="top_mean", yerr="top_std", legend=False,
                    capsize=2, fmt="o-", color="b",
                    rot=90, ax=axes[0])
    axes[0].set_xticks(np.arange(len(df_summary)))
    axes[0].set_xticklabels(df_summary.index)
    axes[0].set_xlabel("Voting rules")
    axes[0].set_ylabel("Mean scores")
    axes[0].set_title("Top mean")
    axes[0].grid(color="gray", linestyle="dashed", linewidth=0.1)
    df_summary.plot(y="topn_mean", yerr="topn_std", legend=False,
                    capsize=2, fmt="o-", color="g",
                    rot=90, ax=axes[1])
    axes[1].set_xticks(np.arange(len(df_summary)))
    axes[1].set_xticklabels(df_summary.index)
    axes[1].set_xlabel("Voting rules")
    axes[1].set_ylabel("Mean scores")
    axes[1].set_title(f"Top{num_topn} mean")
    axes[1].grid(color="gray", linestyle="dashed", linewidth=0.1)
    fig.suptitle(
        f"{num_voters} voters voting for {num_candidates} {voter_model}-candidates\n "
        f"{number_iterations} iterations" + (f" distort rate:{distort_rate}" if distort_rate != 0.0 else ""))
    if save_figure:
        plt.savefig(
            f"figures/scores_{num_candidates}_{num_voters}_{voter_model}_{number_iterations}_{distort_rate if distort_rate != 0.0 else None}.png",
            format="png", dpi=500)

    # Instantiate tmp file
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format="png", dpi=300)
    encoded = b64encode(tmpfile.getvalue()).decode("utf-8")
    return encoded
