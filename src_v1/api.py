import feedparser
import pandas as pd
from langchain.tools import tool


########## Helpers/API ##########
def gen_search_string_from_list(list, sep="|"):
    return sep.join(list)


def filter_df_by_col(df, col, search_string):
    df = df[df[col].str.contains(search_string)]
    return df


def filter_df_by_row(df, search_string):
    return df.filter(like=search_string, axis=0)


########## Data ##########
# data = pd.read_csv("artikel-fiktiv.csv")
# filtered_data = filter_df_by_col(data, "tags", "Polizei")
# ------------------------------- #

# prompts = pd.read_csv("prompts.csv")
# print(filter_df_by_col(prompts, "base-prompt", gen_search_string_from_list(["Bayer", "Polizei", "Berlin"])))


########## RSS Feed ##########
@tool
def get_rss_feed(url: str ="https://www.imensa.de/feeds/pois/ham13/speiseplan.rss") -> str:
    """Get RSS-Feed for Mensa Stellingen"""
    return feedparser.parse(url)
