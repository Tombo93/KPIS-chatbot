import feedparser
from langchain.tools import tool



########## Pandas DF  ##########
def gen_search_string_from_list(list, sep="|"):
    """Example usage:
        gen_search_string_from_list(["Bayer", "Polizei", "Berlin"]))
        returns  "Bayer|Polizei|Berlin"
    """
    return sep.join(list)


def filter_df_by_col(df, col, search_string):
    df = df[df[col].str.contains(search_string)]
    return df


def filter_df_by_row(df, search_string):
    return df.filter(like=search_string, axis=0)


########## RSS Feed ##########
@tool
def get_rss_feed(url: str ="https://www.imensa.de/feeds/pois/ham13/speiseplan.rss") -> str:
    """Get RSS-Feed for Mensa Stellingen"""
    return feedparser.parse(url)
