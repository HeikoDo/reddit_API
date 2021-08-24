import json
import pandas as pd
import requests


filter = "all-crypto"  # all-stocks, all


def get_apewisdom(filter):
    try:
        base_url = f"https://apewisdom.io/api/v1.0/filter/{filter}"
        request = requests.get(base_url, headers={"User-agent": "yourbot"})
    except:
        print("An Error Occured")
    return request.json()


def get_names(r):
    """
    Get a List of post titles
    """
    names = []
    for name in r["results"]:
        x = name["name"]
        name.append(x)
    return name


def get_results(r):
    """
    Create a DataFrame Showing Name, Rank, Ticker, Upvotes, Mentions, Mentions 24h ago
    """
    myDict = {}
    for name in r["results"]:
        myDict[name["name"]] = {
            "rank": name["rank"],
            "ticker": name["ticker"],
            "upvotes": name["upvotes"],
            "mentions": name["mentions"],
            "mentions_24h_ago": name["mentions_24h_ago"],
        }
    df = pd.DataFrame.from_dict(myDict, orient="index")
    df["rank"] = df["rank"].astype(int)
    df["upvotes"] = df["upvotes"].astype(int)
    df["mentions"] = df["mentions"].astype(int)
    df["mentions_24h_ago"] = df["mentions_24h_ago"].astype(int)

    df["delta_mentions_24h"] = df["mentions"] - df["mentions_24h_ago"]
    df = df[~(df["upvotes"] <= 1000)]
    df = df.sort_values(by=["delta_mentions_24h"], ascending=False)
    return df


if __name__ == "__main__":
    r = get_apewisdom(filter)
    df = get_results(r)

print(df.head(100))
