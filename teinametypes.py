from lxml import etree
from pprint import pprint
from plotly.colors import make_colorscale
import plotly.graph_objs as go
import glob
import json
import re

from utils.matching import dpts, provinces, colonies, countries, events


# ---------------------------------------------------------------------------------------
# get which tei:names belong to a certain type (provinces, countries, people names...)
# and visualise it
# ---------------------------------------------------------------------------------------


ns = {"tei": "http://www.tei-c.org/ns/1.0"}  # tei namespace

def getnametype():
  """
  create a dictionnary mapping to different types of tei:names a number of
  occurrences; print the string representation of those tei:names
  """
  files = glob.glob("./in/*.xml")
  parser = etree.XMLParser(remove_blank_text=True)
  out = {
    "divers" : 0,
    "empty_name" : 0,
    "geo": 0,
    "events" : 0,
    "name": 0
  }  # dict mapping to a type the n° of tei:names in that type
  snowflakes = {
    "dpts" : [],
    "geo": [],
    "events" : []
  }  # to print the tei rpr of the special (aka, non-person tei-names)
  for f in files:
    with open(f, mode="r") as fh:
      tree = etree.parse(fh, parser=parser)
      names = tree.xpath(r".//tei:body//tei:name", namespaces=ns)
      for n in names:
	# if there is text
        if n.text:
          t = n.text.lower()
          if re.search(r"^(le|la)\sm[êe]me\.?$", t) \
              or re.search(r"^(documents?|(divers)|\s)+$", t) \
              or re.search(r"chartes?", t):
            out["divers"] += 1
          elif any(d in t for d in dpts)\
              or any(p in t for p in provinces)\
              or any(c in t for c in colonies)\
              or any(c in t for c in countries.keys()):
            out["geo"] += 1
            snowflakes["geo"].append(str(etree.tostring(
                                      n, xml_declaration=False, encoding="utf-8").decode("utf-8")
            ))
          elif any(e in t for e in events.keys()):
            out["events"] += 1
            snowflakes["events"].append(str(etree.tostring(
                                      n, xml_declaration=False, encoding="utf-8").decode("utf-8")
            ))
          else:
            out["name"] += 1
        else:
          out["empty_name"] += 1

  # write the dict to file
  with open("out/teinametypes.json", mode="w") as fh:
    json.dump(snowflakes, fh, indent=4)

  return out


def nametypes_tograph(data):
  """
  visualise out (the dict created at the previous step)
  :param data: the data to visualize (aka, the out dict)
  """
  colors = {"cream": "#fcf8f7", "blue": "#0000ef", "burgundy1": "#890c0c", "burgundy2": "#a41a6a", "pink": "#ff94c9"}
  scale = make_colorscale([colors["blue"], colors["burgundy2"]])  # create a colorscale
  layout = {
        "paper_bgcolor": colors["cream"],
        "plot_bgcolor": colors["cream"],
        "margin": {"l": 5, "r": 10, "t": 5, "b": 10},
        "showlegend": False,
        "xaxis": {"anchor": "x", "title": {"text": r"$\text{Type de tei:name}$"}},
        "yaxis": {"anchor": "x", "title": {"text": r"$\text{Nombre d'occurrences}$"}},
  }
  x_values = {
    "divers" : r"$\text{Divers}$",
    "empty_name" : r"$\text{Element vide}$",
    "geo" : r"$\text{Nom geographique}$",
    "events" : r"$\text{Evenement historique}$",
    "name" : r"$\text{Nom de personne}$"
  }

  # sort data by ascending values
  data = {k: v for v, k in sorted((value, key) for (key, value) in data.items())}
  y = list(data.values())
  x = [x_values[k] for k in data.keys()]
  fig = go.Figure(
    data=[go.Bar(
                x=x,
                y=y,
                marker={"color": y, "colorscale": scale, "cauto": False,
                        "cmin": 0, "cmax": max(y), "colorbar": {"xpad": 0, "ypad": 0}},
                text=[str(i) for i in y],
                width=0.5
    )],
    layout=go.Layout(layout)
  )
  fig.show()
  fig.write_image("out/teinametypes.png", width=700, height=1000)

if __name__ == "__main__":
  data = getnametype()
  nametypes_tograph(data)
