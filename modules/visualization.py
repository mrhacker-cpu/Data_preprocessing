import matplotlib.pyplot as plt
import seaborn as sns

def plot_multi_hist(df):
    fig, axs = plt.subplots(2, 2, figsize=(6, 5))

    num_cols = df.select_dtypes(include='number').columns[:4]

    for i, col in enumerate(num_cols):
        axs[i//2, i%2].hist(df[col])
        axs[i//2, i%2].set_title(col)

    return fig

def plot_heatmap(df):
    plt.figure(figsize=(6, 4))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
    return plt.gcf()