#!/usr/bin/env python3

import pandas as pd
import csv

input_file = "C://Users//odoniku//Documents//GitHub//complaints_analysis_CC//complaints.csv"
output_file = "C://Users//odoniku//Documents//GitHub//complaints_analysis_CC//report.csv"
########################################################################################################################
def round_num(num, precision=0):
    """
    This function will create the rounding logic from floats to integers using the standard rounding convention. 0.5 --> 1.
    num: the number to round
    precision: how many decimal places to round. So precision of 0 will be an integer
    """
    # Edge case-1: negative precision will not operate on the number provided
    if precision < 0:
        return num
    # Edge case-2: values provided that are neither integers nor floats will not be operated on
    elif type(num) not in [int, float]:
        return num
    else:
        if precision == 0:
            if type(num) == int:
                return num
            else:
                if num < 0:
                    return int(num - 0.5)
                else:
                    return int(num + 0.5)
        else:
            if precision > 0:
                if type(num) == int:
                    return num
                else:
                    return float("{0:.{1}f}".format(num, precision))
########################################################################################################################
data = pd.read_csv(input_file)
data["year"] = pd.to_datetime(data["Date received"]).dt.year
data["Product"] = data["Product"].str.lower()
data.drop_duplicates(subset="Complaint ID", inplace=True)
grouped = data.groupby(["Product", "year"]).size().reset_index()
grouped_company = data.groupby(["Product", "year"]).Company.agg('unique').reset_index()
grouped_company["Company"] = grouped_company["Company"].str.len()
grouped["num_companies"] = grouped_company["Company"]
grouped_coy = data.groupby(["Product", "year","Company"]).size().reset_index().groupby(["Product", "year"]).max().reset_index()
grouped_coy.columns = ["Product", "year", "Company", "max_complaints_coy"]
grouped["max_complaints_comapny"] = grouped_coy["max_complaints_coy"]
grouped.columns = ["Product", "year", "num_complaints", "num_companies", "max_complaints_comapny"]
grouped["max_percent_complaints_company"] = grouped["max_complaints_comapny"] * 100 / grouped["num_complaints"]
grouped["max_percent_complaints_company"] = grouped["max_percent_complaints_company"].apply(lambda x:round_num(x,0))
output = grouped[["Product", "year", "num_complaints", "num_companies", "max_percent_complaints_company"]]
output.to_csv(output_file, index=False, header=False, quoting=csv.QUOTE_MINIMAL)


