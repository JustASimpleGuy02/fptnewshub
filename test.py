from serpapi import GoogleSearch
import json

params = {
    "api_key": "...",           # https://serpapi.com/manage-api-key
    "engine": "google",         # serpapi parsing engine
    "q": "đại học fpt",     # search query
    "gl": "vn",                 # country from where search comes from
    "tbm": "nws"                # news results
    # other parameters such as language `hl` and number of news results `num`, etc.
}

search = GoogleSearch(params)   # where data extraction happens on the backend
results = search.get_dict()     # JSON - > Python dictionary
print(results)
# for result in results["news_results"]:
    # print(json.dumps(results, indent=2))
