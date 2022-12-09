"""
Utils
----------------
- Plotting scores
- Converters
"""

import pandas as pd
import matplotlib.pylab as plt

def plot_final_results(name, results, num_voters, num_candidates, number_iterations):
    # Plot the scores for all voting rules
    df = pd.DataFrame.from_dict(results)
    df = df.rename(columns={0: "Top"})
    df = pd.concat([df.drop(['Top'], axis=1), df['Top'].apply(pd.Series)], axis=1)
    df['top_mean'] = df["top"].mean(axis=0)
    df['top_std']  = df["top"].std(axis=0)
    df['topn_mean'] = df["topn"].mean(axis=0)
    df['topn_std']  = df["topn"].std(axis=0)
    fig, ax = plt.subplots()
    df.plot(y = "top_mean",  yerr = "top_std",  legend = False,  capsize=2, fmt='o-', color='b', capthick=0.2, title = "Scores")
    # df.plot(y = "topn_mean", yerr = "topn_std", legend = False, capsize=2, fmt='o-', color='g', capthick=0.2, title = "Scores")
    # df.plot(y = ["top_mean", "topn_mean"], legend = False,title = "Scores")
    plt.xlabel("Voting rules")
    plt.ylabel("Mean scores")
    plt.xticks(range(0,len(df.index)), df.index)
    plt.grid(color='gray', linestyle='dashed', linewidth=0.1)
    plt.title("{} voters voting for {} {}-candidates\n {} iterations".format(num_voters, num_candidates, name, number_iterations))
    plt.savefig("figures/scores_{}.png".format(name), format='png', dpi=500)

# int-str converters

def int_list_to_str(l):
    return ','.join(map(str, l))

def str_list_to_in(l):
    return list(map(int, l.split(",")))

#-- print (sorted(str_list_to_in('1,2,5,4,3,0,6')))
