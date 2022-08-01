import json
from operator import itemgetter
from plotly.colors import make_colorscale
import plotly.graph_objs as go

with open("in/wikidata_enrichments.json", mode="r") as fh:
  data = json.load(fh)

# build instance dict
instance_counter_full = {}
for entry in data.values():
  for i in entry["instanceL"]:
    if i not in instance_counter_full.keys():
      instance_counter_full[i] = 1
    else:
      instance_counter_full[i] += 1

# order dict
instance_counter = dict(sorted(instance_counter_full.items(), key=itemgetter(1), reverse=True))

# replace less used items by "other"
n = 0
instance = dict()
instance["other"] = 0
for k, v in instance_counter.items():
  n += 1
  if n > 20:
    instance["other"] += v
  else:
    instance[k] = v

# order dict
instance = dict(sorted(instance.items(), key=itemgetter(1)))

# build the graph
colors = {"white": "#ffffff", "cream": "#fcf8f7", "blue": "#0000ef", "burgundy1": "#890c0c", "burgundy2": "#a41a6a", "pink": "#ff94c9"}
scale = make_colorscale([colors["blue"], colors["burgundy2"]])  # create a colorscale
colorbar = {"xpad": 0, "ypad": 0}
x = [r"$\text{%s (%s occurrences)}$" % (k, v) for k, v in instance.items()]
y = list(instance.values())
layout = {
    "paper_bgcolor": colors["white"],
    "plot_bgcolor": colors["cream"],
    "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
    "showlegend": False,
    "xaxis": {"anchor": "x",
              "title": {"text": r"$\text{Instances auxquelles appartiennent les %s " % len(data.keys())
				 + "entitées récupérées sur Wikidata}$"}},
    "yaxis": {"anchor": "x", "title": {"text": r"$\text{Nombre d'entités}$"}}
}
fig = go.Figure(
              data=go.Bar(x=x, y=y,
                          marker={"color": y, "colorscale": scale, "colorbar": colorbar,
                                  "cauto": False, "cmin": 0.00, "cmax": 1000.00}
                          ),
              layout=go.Layout(layout)
)
fig.update_xaxes(tickangle=45)
fig.show()
fig.write_image("out/fig_wikidata_instances.png", width=1000, height=1000)
