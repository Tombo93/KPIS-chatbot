import pandas as pd


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

prompts = pd.read_csv("prompts.csv")
print(filter_df_by_col(prompts, "base-prompt", gen_search_string_from_list(["Bayer", "Polizei", "Berlin"])))