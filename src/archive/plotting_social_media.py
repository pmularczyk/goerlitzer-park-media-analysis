# ------------- Libraries ------------- #
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------- Paths ------------- #
facebook = r"D:\git\Goerli\resources\raw_xls\Facebook_Analyse.xls"
twitter = r"D:\git\Goerli\resources\raw_xls\Tweets_Analyse.xls"
out_img_facebook_barh = r"C:\Users\Patrick\Documents\goerlitzer_park\facebook_barhorizontal.png"
out_img_twitter_barh = r"C:\Users\Patrick\Documents\goerlitzer_park\twitter_barhorizontal.png"

out_img_facebook_bar = r"C:\Users\Patrick\Documents\goerlitzer_park\facebook_bar.png"
out_img_twitter_bar = r"C:\Users\Patrick\Documents\goerlitzer_park\twitter_bar.png"

out_img_facebook_sub = r"C:\Users\Patrick\Documents\goerlitzer_park\facebook_subplot.png"
out_img_twitter_sub = r"C:\Users\Patrick\Documents\goerlitzer_park\twitter_subplot.png"

# ------------- Utility Function ------------- #
def plot_count_per_barh(col, category):
    for i, v in enumerate(df[col]):
        ax.text(v + 3, i + .15, f"{category}: " + str(int(v)), fontsize=15, color='dimgrey')
        
def plot_count_per_bar(col, category):
    for i, v in enumerate(df[col]):
        ax.text(i, v + 800,
                f"{category}: " + str(int(v)),
                fontsize=15,
                color='dimgrey',
                horizontalalignment='center',
                verticalalignment='center',
                rotation=90)


# ------------- Prepare DataFrame ------------- #
df = pd.read_excel(facebook, parse_dates=[1])
df = df.fillna(0)
keep = ["Date", "Author", "Likes", "Kommentare", "Geteilt"]
df = df[keep]
drop = df[(df["Date"] == 0) | (df["Author"] == 0)].index
df = df.drop(drop)
df["post"] = df.Author + "_" + df.Date.astype(str).apply(lambda entry: entry[:10])
drop2 = ["Date", "Author"]
df = df.drop(drop2, axis=1)
df = df.set_index("post")

# ------------- Plot Data ------------- #
ax = df.plot.barh(figsize=(22, 12))
plt.grid(axis="x", alpha=0.55)
plt.yticks(fontsize=18)
plt.xticks(fontsize=16)
plt.title("Kommentare und Likes Facebook", fontsize=18)
ax.invert_yaxis()
plot_count_per_barh("Likes", "Likes")
plt.tight_layout()
plt.savefig(out_img_facebook_barh, dpi=300, orientation="landscape")
plt.show()

# ------------- Plot Data ------------- #
ax = df.plot.bar(figsize=(18, 12))
plt.grid(axis="y", alpha=0.55)
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
plt.title("Kommentare und Likes Facebook", fontsize=18)
plot_count_per_bar("Likes", "Likes")
plt.tight_layout()
plt.savefig(out_img_facebook_bar, dpi=300, orientation="landscape")
plt.show()

# ------------- Plot Data ------------- #
ax = df.plot.bar(figsize=(18, 12), subplots=True)
ax[1].legend(loc=2)
plt.title("Kommentare und Likes Facebook", fontsize=18)
plt.tight_layout()
plt.savefig(out_img_facebook_sub, dpi=300, orientation="landscape")
plt.show()

# ------------- Utility Function ------------- #
def plot_count_per_barh(col, category):
    for i, v in enumerate(df[col]):
        ax.text(v + 3, i + .15, f"{category}: " + str(int(v)), fontsize=15, color='dimgrey')
        
def plot_count_per_bar(col, category):
    for i, v in enumerate(df[col]):
        ax.text(i + .05, v + 350,
                f"{category}: " + str(int(v)),
                fontsize=15,
                color='dimgrey',
                rotation=90)

# ------------- Prepare DataFrame ------------- #
df = pd.read_excel(twitter, parse_dates=[1])
df = df.fillna(0)
keep = ["Date", "Author", "Replies", "Retweets", "Likes"]
df = df[keep]
df["post"] = df.Author + "_" + df.Date.astype(str).apply(lambda entry: entry[:10])
drop2 = ["Date", "Author"]
df = df.drop(drop2, axis=1)
df = df.set_index("post")

# ------------- Plot Data ------------- #
ax = df.plot.barh(figsize=(22, 12))
plt.grid(axis="x", alpha=0.55)
plt.yticks(fontsize=18)
plt.xticks(fontsize=16)
plt.title("Likes und Retweets Twitter", fontsize=18)
ax.invert_yaxis()
plot_count_per_barh("Likes", "Likes")
plt.tight_layout()
plt.savefig(out_img_twitter_barh, dpi=300, orientation="landscape")
plt.show()

# ------------- Plot Data ------------- #
ax = df.plot.bar(figsize=(18, 12))
plt.grid(axis="y", alpha=0.55)
plt.yticks(fontsize=16)
plt.xticks(fontsize=16)
plt.title("Likes und Retweets Twitter", fontsize=18)
plot_count_per_bar("Likes", "Likes")
plt.tight_layout()
plt.savefig(out_img_twitter_bar, dpi=300, orientation="landscape")
plt.show()

# ------------- Plot Data ------------- #
ax = df.plot.bar(figsize=(18, 12), subplots=True)
ax[1].legend(loc=2)
plt.title("Likes und Retweets Twitter", fontsize=18)
plt.tight_layout()
plt.savefig(out_img_twitter_sub, dpi=300, orientation="landscape")
plt.show()


# --------------------------------------- #
#
#       Creating and plotting aggregates
#
# --------------------------------------- #

out_img_facebook_aggr_barh = r"C:\Users\Patrick\Documents\goerlitzer_park\facebook_aggregated_horizontal.png"
out_img_facebook_aggr_bar = r"C:\Users\Patrick\Documents\goerlitzer_park\facebook_aggregated_barplot.png"
out_img_facebook_aggr_sub = r"C:\Users\Patrick\Documents\goerlitzer_park\facebook_aggregated_subplot.png"


# ------------- Prepare DataFrame ------------- #
df = pd.read_excel(facebook, parse_dates=[1])
df = df.fillna(0)
keep = ["Date", "Author", "Likes", "Kommentare", "Geteilt", "Thema"]
df = df[keep]
drop = df[(df["Date"] == 0) | (df["Author"] == 0)].index
df = df.drop(drop)
drop2 = ["Date", "Author"]
df = df.drop(drop2, axis=1)
df = df.groupby("Thema").agg({"Likes": "sum", "Kommentare": "sum", "Geteilt": "sum"})

# ------------- Utility Function ------------- #
def plot_count_per_barh(col, category):
    for i, v in enumerate(df[col]):
        ax.text(v + 15, i - 0.10, f"{category}: " + str(int(v)), fontsize=15, color='dimgrey')
        
def plot_count_per_bar(col, category):
    for i, v in enumerate(df[col]):
        ax.text(i - 0.25, v + 600,
                f"{category}: " + str(int(v)),
                fontsize=15,
                color='dimgrey',
                horizontalalignment='center',
                verticalalignment='center',
                rotation=0)


title = "Kommentare und Likes pro Thema Facebook"
# ------------- Plot Data ------------- #
ax = df.plot.barh(figsize=(22, 12))
plt.grid(axis="x", alpha=0.55)
plt.yticks(fontsize=18)
plt.xticks(fontsize=16)
plt.title(title, fontsize=18)
ax.invert_yaxis()
plot_count_per_barh("Likes", "Likes")
plt.tight_layout()
plt.savefig(out_img_facebook_aggr_barh, dpi=300, orientation="landscape")
plt.show()

# ------------- Plot Data ------------- #
ax = df.plot.bar(figsize=(18, 12))
plt.grid(axis="y", alpha=0.55)
plt.yticks(fontsize=16)
plt.xticks(fontsize=16, rotation=45)
plt.title(title, fontsize=18)
plot_count_per_bar("Likes", "Likes")
plt.tight_layout()
plt.savefig(out_img_facebook_aggr_bar, dpi=300, orientation="landscape")
plt.show()

# ------------- Plot Data ------------- #
ax = df.plot.bar(figsize=(18, 12), subplots=True)
ax[1].legend(loc=2)
plt.title(title, fontsize=18)
plt.tight_layout()
plt.savefig(out_img_facebook_aggr_sub, dpi=300, orientation="landscape")
plt.show()


out_img_twitter_aggr_barh = r"C:\Users\Patrick\Documents\goerlitzer_park\twitter_aggregated_horizontal.png"
out_img_twitter_aggr_bar = r"C:\Users\Patrick\Documents\goerlitzer_park\twitter_aggregated_barplot.png"
out_img_twitter_aggr_sub = r"C:\Users\Patrick\Documents\goerlitzer_park\twitter_aggregated_subplot.png"

# ------------- Prepare DataFrame ------------- #
df = pd.read_excel(twitter, parse_dates=[1])
df = df.fillna(0)
keep = ["Date", "Author", "Replies", "Retweets", "Likes", "Thema"]
df = df[keep]
df["post"] = df.Author + "_" + df.Date.astype(str).apply(lambda entry: entry[:10])
drop2 = ["Date", "Author"]
df = df.drop(drop2, axis=1)
df = df.groupby("Thema").agg({"Likes": "sum", "Replies": "sum", "Retweets": "sum"})

# ------------- Utility Function ------------- #
def plot_count_per_barh(col, category):
    for i, v in enumerate(df[col]):
        ax.text(v + 15, i - 0.10, f"{category}: " + str(int(v)), fontsize=15, color='dimgrey')
        
def plot_count_per_bar(col, category):
    for i, v in enumerate(df[col]):
        ax.text(i - 0.45, v + 200,
                f"{category}: " + str(int(v)),
                fontsize=15,
                color='dimgrey',
                rotation=0)

title = "Likes und Retweets Twitter pro Thema"
# ------------- Plot Data ------------- #
ax = df.plot.barh(figsize=(22, 12))
plt.grid(axis="x", alpha=0.55)
plt.yticks(fontsize=18)
plt.xticks(fontsize=16)
plt.title(title, fontsize=18)
ax.invert_yaxis()
plot_count_per_barh("Likes", "Likes")
plt.tight_layout()
plt.savefig(out_img_twitter_aggr_barh, dpi=300, orientation="landscape")
plt.show()

# ------------- Plot Data ------------- #
ax = df.plot.bar(figsize=(18, 12))
plt.grid(axis="y", alpha=0.55)
plt.yticks(fontsize=16)
plt.xticks(fontsize=16, rotation=45)
plt.title(title, fontsize=18)
plot_count_per_bar("Likes", "Likes")
plt.tight_layout()
plt.savefig(out_img_twitter_aggr_bar, dpi=300, orientation="landscape")
plt.show()

# ------------- Plot Data ------------- #
ax = df.plot.bar(figsize=(18, 12), subplots=True)
ax[1].legend(loc=2)
plt.title(title, fontsize=18)
plt.tight_layout()
plt.savefig(out_img_twitter_aggr_sub, dpi=300, orientation="landscape")
plt.show()