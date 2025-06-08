import requests

PHP_API_URL = "https://www.wikidata.org/w/api.php"


def simple_query(name):
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "search": name,
        "limit": 10,
        "language": "sv",
        "uselang": "sv",
        "type": "item",
    }
    response = requests.get(PHP_API_URL, params=params).json()
    data = response["search"]

    return [
        {key: i[key] for key in ["id", "label", "description"] if key in i}
        for i in data
    ]


def query_wikidata(name):
    """
    Queries the Wikidata API for people with the given name.

    Args:
        name (str): The name to search for.

    Returns:
        list: A list of people's names found in Wikidata.
    """
    query = f"""
    SELECT DISTINCT ?item ?label
    WHERE
    {{
    SERVICE wikibase:mwapi
    {{
        bd:serviceParam wikibase:endpoint "www.wikidata.org";
                        wikibase:api "Generator";
                        mwapi:generator "search";
                        mwapi:gsrsearch "inlabel:{name}"@sv;
                        mwapi:gsrlimit "max".
        ?item wikibase:apiOutputItem mwapi:title.
    }}
    ?item rdfs:label ?label. FILTER( LANG(?label)="sv" )
    ?item wdt:P31 wd:Q5 .
    }}
    """
    url = "https://query.wikidata.org/sparql"
    try:
        response = requests.get(url, params={"query": query, "format": "json"})
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data.get("results", {}).get("bindings", []):
            results.append(
                f'{item["label"]["value"]} ({item["item"]["value"].split("/")[-1]})'
            )
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error querying Wikidata: {e}")
        return []


def query_organisation_wikidata(name):
    """
    Queries the Wikidata API for people with the given name.

    Args:
        name (str): The name to search for.

    Returns:
        list: A list of people's names found in Wikidata and their Wikidata ID.
    """
    query = f"""
    SELECT DISTINCT ?item ?label
    WHERE
    {{
    SERVICE wikibase:mwapi
    {{
        bd:serviceParam wikibase:endpoint "www.wikidata.org";
                        wikibase:api "Generator";
                        mwapi:generator "search";
                        mwapi:gsrsearch "inlabel:{name}"@sv;
                        mwapi:gsrlimit "max".
        ?item wikibase:apiOutputItem mwapi:title.
    }}
    ?item rdfs:label ?label. FILTER( LANG(?label)="sv" )
    ?item wdt:P31 wd:Q43229 .
    }}
    """
    url = "https://query.wikidata.org/sparql"
    try:
        response = requests.get(url, params={"query": query, "format": "json"})
        response.raise_for_status()
        data = response.json()
        results = []
        for item in data.get("results", {}).get("bindings", []):
            results.append(
                f'{item["label"]["value"]} ({item["item"]["value"].split("/")[-1]})'
            )
        return results
    except requests.exceptions.RequestException as e:
        print(f"Error querying Wikidata: {e}")
        return []


# Test Wikidata query
wikidata_results = simple_query("Rud Pedersen")
print(f"Wikidata results for Rud Pedersen: {wikidata_results}")
print("-" * 20)
