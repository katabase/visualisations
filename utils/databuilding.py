from statistics import mean, quantiles
import json
import re

from .conversion_tables import term_types


# ---------------------------------------------------
# prepare data to make visualisations from json files
# ---------------------------------------------------


# general variables
indir = "in"
with open(f"{indir}/export_catalog.json", mode="r") as f:
    js_cat = json.load(f)
with open(f"{indir}/export_item.json", mode="r") as f:
    js_item = json.load(f)


def databuild():
    """
    prepare the data to build visualisations on prices
    :return: a lot of dicts
    """
    pdict_ls_cat = {}  # dictionnary mapping to a year a list of catalogue prices to calculate totals, medians + means
    pdict_ls_item = {}  # dictionnary mapping to a year a list of item prices, to calculate median and mean values
    cdict_fix_item = {}  # dictionary mapping to a year the total of fixed price items sold (cdict = count dictionary)
    cdict_auc_item = {}  # dictionary mapping to a year the total of non fixed price items sold: the auction items
    quart_ls_item = {}  # dictionary mapping to a 5 year range its quartiles
    cdict_term_item = {}  # dict mapping to a term (mss type) a dict that maps year to the n° of occurrences of that type
    pdict_auth_item = {}  # dictionnary mapping to an author name a dict {year: list of all items price}
    sort_fix_item = {}  # "sort" dictionaries below are used to sort the above dicts by year
    sort_auc_item = {}
    sort_ls_item = {}
    sort_ls_cat = {}

    # create a new dictionnary: pdict_ls_cat, a dictionnary mapping to a year the list of total catalogue
    # prices ; from that list, we will be able to calculate
    # - the total price of all items sold
    # - the median price of a full catalogue per year
    # - the average price of a full catalogue
    for c in js_cat:  # loop over every catalogue item
        if "total_price_c" in js_cat[c] and "sell_date" in js_cat[c]:
            date = re.findall(r"\d{4}", js_cat[c]["sell_date"])[0]  # year of the sale
            # if it is the first time a date is encountered, add it to the dictionnaries
            if date not in list(pdict_ls_cat.keys()):
                pdict_ls_cat[date] = [js_cat[c]["total_price_c"]]
            else:
                pdict_ls_cat[date].append(js_cat[c]["total_price_c"])
            figpath = True  # at this point, it is certain that figures are created

    # create 4 dictionnaries:
    # - pdict_ls_item: list of item prices per year
    # - cdict_fix_item: number of fixed price items sold per year
    # - cdict_auc_item: number of non-fixed price items sold per year
    # - term_item: {year: {term: number of items}}
    ls = []
    for i in js_item:
        # append data to the dicts

        if "sell_date" in js_item[i]:
            date = re.findall(r"\d{4}", js_item[i]["sell_date"])[0]  # year of the sale
            # calculate the number of fixed price and auction items put up for sale every year
            if "price_c" in list(js_item[i].keys()):
                if date not in cdict_fix_item.keys():
                    cdict_fix_item[date] = 1
                else:
                    cdict_fix_item[date] += 1
            else:
                if date not in cdict_auc_item.keys():
                    cdict_auc_item[date] = 1
                else:
                    cdict_auc_item[date] += 1

            # if there is price info on an item, create pdict_ls_item
            if "price_c" in js_item[i] \
                    and "currency" in js_item[i]:
                if date not in pdict_ls_item.keys():
                    pdict_ls_item[date] = [js_item[i]["price_c"]]
                elif date in pdict_ls_item.keys():
                    pdict_ls_item[date].append(js_item[i]["price_c"])

            # build term_item
            if js_item[i]["term"] is not None:
                # find the actual name for a term
                for k, v in term_types.items():
                    if v == js_item[i]["term"]:
                        term = k
                # append it to the dict
                if term not in cdict_term_item.keys():
                    cdict_term_item[term] = {date: 1}
                else:
                    if date in cdict_term_item[term].keys():
                        cdict_term_item[term][date] += 1
                    else:
                        cdict_term_item[term][date] = 1

            if js_item[i]["author"] is not None and "price_c" in js_item[i].keys():
                # extract author and price; normalize author name
                author = js_item[i]["author"].split()
                auth = ""
                for a in author:
                    # special case of roman numers
                    if not re.search(r"^[MLCDVIX]+$", a):
                        auth += f"{a[0].upper()}{a[1:].lower()} "
                    else:
                        auth += a
                auth = re.sub(r"\s+", " ", auth).strip()
                price = js_item[i]["price_c"]
                if auth not in pdict_auth_item.keys():
                    pdict_auth_item[auth] = {date: [price]}
                else:
                    if date in pdict_auth_item[auth].keys():
                        pdict_auth_item[auth][date].append(price)
                    else:
                        pdict_auth_item[auth][date] = [price]

    # finalise the data creation ; for some reason, the lengths of catalogues vary depending on the
    # source catalogue and what is being calculated ; the keys also vary from one dictionary to another.
    # in turn, we need to loop over the different kinds of dicts separately
    datelist = sorted(set(pdict_ls_cat.keys()))  # sorted list of dates on which we have sale info
    # sort the price per catalog dictionnaries
    for k in sorted(list(pdict_ls_cat.keys())):
        sort_ls_cat[k] = pdict_ls_cat[k]
    pdict_ls_cat = sort_ls_cat
    # sort the price per item dictionnaries
    for k in sorted(list(pdict_ls_item.keys())):
        sort_ls_item[k] = pdict_ls_item[k]
    pdict_ls_item = sort_ls_item
    # sort the cdict_* dictionnaires
    for k in sorted(list(cdict_fix_item.keys())):
        sort_fix_item[k] = cdict_fix_item[k]
    for k in sorted(list(cdict_auc_item.keys())):
        sort_auc_item[k] = cdict_auc_item[k]
    cdict_auc_item = sort_auc_item
    cdict_fix_item = sort_fix_item
    # create data for the box charts: group pdict_ls_item values per 5 year range + calculate quartiles for each range
    group_ls_item = sorter(pdict_ls_item)  # dictionary mapping to a 5 year range the list prices for that range
    for k, v in group_ls_item.items():
        quart_ls_item[str(k)] = quantiles(v)
    # we don't reorder term_item, there's no point.

    return datelist, pdict_ls_cat, pdict_ls_item, cdict_auc_item, cdict_fix_item, quart_ls_item, \
        cdict_term_item, pdict_auth_item


def sorter(input_dict):
    """
    group the values of input_dict in 5 year ranges. input_dict is a dictionnary mapping to
    each year a list of item prices. the values of input_dict must be non-nested lists containing integers
    only (no lists within lists).
    sorter groups the keys of input_dict in 5 year ranges (1821-1826, 1826-1830...) ;
    the keys of output_dict are the average between floor and roof values for a
    5 year range (1821-1826 => 1823); the values of output_dict are a list of item prices
    for that 5 year range

    :param input_dict: the input dictionary to sort
    :return: output_dict, a dictionnary mapping to an average year the item prices for a range
    """
    output_dict = {}
    for d in input_dict.keys():
        d = int(d)
        last = d % 10
        if last >= 6:
            floor = (d - last) + 6
            roof = d + (10 - last)
            k = mean([floor, roof])
        else:
            floor = (d - last) + 1
            roof = (d - last) + 5
            k = mean([floor, roof])
        if k not in output_dict.keys():
            output_dict[k] = input_dict[str(d)]
        else:
            for v in input_dict[str(d)]:
                output_dict[k].append(v)
    return output_dict


if __name__ == "__main__":
    databuild()