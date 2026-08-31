import networkx as nx
import json

raw_data = json.load(open("ets2_data.json", "r", encoding = "utf-8"))
G = nx.Graph()
for country1 in raw_data:
    if not country1.startswith("$"):
        G.add_edges_from([(country1, country2) for country2 in raw_data[country1]["connects_to"]])
for country in G:
    G.nodes[country]["color"] = "red"
b = True
if b:
    # My countries
    obtained_countries = ["Andorra", "Lebanon", "Sweden", "Faroe Islands", "Jordan", "Montenegro", "Austria", "Serbia", "Spain", "Greece", "Bulgaria", "Norway", "Czech Republic", "Tunisia", "Slovenia", "Denmark", "Iraq", "Croatia", "Portugal", "Estonia", "United Kingdom", "Morocco", "Switzerland", "Italy", "Jersey", "Türkiye", "Egypt", "Greenland", "Hungary", "Azerbaijan", "Kosovo", "West Bank", "Romania", "Poland", "Latvia", "Syria"]
    finished_countries = ["Morocco", "Tunisia", "Andorra", "Portugal"]
else:
    # Zatsu
    obtained_countries = ["Faroe Islands", "Moldova", "Greece", "Iceland", "Israel", "Denmark", "Kosovo", "Armenia", "Tunisia", "Sweden", "Switzerland", "Bosnia and Herzegovina", "Greenland", "Liechtenstein", "Lebanon", "Kazakshtan", "Finland", "Romania", "Georgia", "Ireland", "North Macedonia", "Cyprus", "Slovenia", "Andorra", "Jordan", "Türkiye", "Italy", "Netherlands", "Hungary"]
    finished_countries = ["Faroe Islands", "Denmark", "Greenland", "Sweden", "Finland"]
to_process = [obtained_countries[0]]
while len(to_process) > 0:
    curr_country = to_process.pop()
    if curr_country in obtained_countries and G.nodes[curr_country]["color"] == "red":
        G.nodes[curr_country]["color"] = "gold" if curr_country in finished_countries else "green"
        to_process.extend([c for c in G.neighbors(curr_country)])
for country in obtained_countries:
    if G.nodes[country]["color"] == "red":
        G.nodes[country]["color"] = "purple"
nx.write_graphml(G.subgraph([x for x in G if G.nodes[x]["color"] in ["green", "gold"]]), "ets2_accessibility_map.graphml")
nx.write_graphml(G, "ets2_graph.graphml")
