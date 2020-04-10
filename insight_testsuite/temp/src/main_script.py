#!/usr/bin/env python3

"""
This script provides an aggregation of complaints filed against companies regarding different financial products. The script will identify the number of complaints filed and how they're spread across different companies by aggregating the total number of complaints for each financial product and year, as well as number of companies receiving a complaint, and the highest percentage of complaints directed at a single company
"""

######################### IMPORT USEFUL MODULES ##########################
# import the necessary python builtin modules...
import sys
import csv
import math
from collections import Counter, defaultdict
from operator import itemgetter
from datetime import datetime

######################## FILES ##########################################

input_file = sys.argv[1]
output_file = sys.argv[2]

######################## INPUT ###########################################
def get_input(input_file):
    """
    This function will read an input csv file into a dictionary using the DictReader Class of the csv module.
    The Date field is converted to year.
    Product field is converted to lower case.
    The data will be contained using a defaultdict.
    Product and year are used as the defaultdict dictionary key.
    input_file: The input csv file.
    """
    with open(input_file, newline='') as csv_input:
        input_reader = csv.DictReader(csv_input)
        duplicate_complaint_id = []
        duplicate_key = []
        complaints = defaultdict(list)
        for i, row in enumerate(input_reader):
            # Check if there are duplicate rows in the input data. "Complaint ID" is assumed to be the unique identifier
            if row["Complaint ID"] not in duplicate_complaint_id:
                c_id = row["Complaint ID"]
                date = row["Date received"]
                try:
                    year = datetime.strptime(date, "%m/%d/%Y").year
                except ValueError as e:
                    print(e)
                    if e:
                        year = datetime.strptime(date, "%Y-%m-%d").year
                product = row["Product"].lower()
                company = row["Company"]
                num_coy = 0
                perc_complaints = 0
                # Check product-year pair existence in dictionary container.
                # If not exist then set num_complaints to 1, otherwise increase the count by 1
                if (product, year) not in duplicate_key:
                    num_complaints = 1
                    complaints[product, year] = [num_complaints, num_coy, perc_complaints, company]
                    duplicate_key.append((product, year))
                else:
                    complaints[product, year].append(company)
                    complaints[product, year][0] += 1
                duplicate_complaint_id.append(c_id)
            else:
                continue
    return complaints


################################ AGGREGATION AND COMPUTATION #################################
def calculate_num_companies(input_file):
    """
    The function will calculate the number of companies that received at least one complaint for each product-year key
    """
    complaints = get_input(input_file=input_file)
    for key, val in complaints.items():
        num_companies = len(set(val[3:]))
        val[1] = num_companies
    return complaints


def calculate_max_percent_complaints(input_file):
    """
    The function will calculate the highest percentage of total complaints filed against one company for each product-year pair.
    """
    with_num_of_companies = calculate_num_companies(input_file=input_file)
    for key, val in with_num_of_companies.items():
        complaint_counter = Counter(val[3:])
        max_complaints = max(complaint_counter.values())
        try:
            percent_complaints = round_num((max_complaints/val[0])*100, 0)
        except ZeroDivisionError:
            percent_complaints = math.nan
        val[2] = percent_complaints
    return with_num_of_companies


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


######################## OUTPUT ###########################################
def generate_output_data(input_file):
    """
    The function will generate the output data using the results of the previous functions.
    """
    output_data = []
    with_max_complaints_company = calculate_max_percent_complaints(input_file=input_file)
    for ind, row in with_max_complaints_company.items():
        output_row = [ind[0], ind[1], row[0], row[1], row[2]]
        output_data.append(output_row)
    sorted_output_data = sorted(output_data, key=itemgetter(0,1))
    return sorted_output_data


######################## EXPORT ###########################################
field_names = ["product", "year", "total_num_complaints", "num_companies, max_percent_complaints_company"]
def process_input_and_export_output():
    """
    The function will export the output data to a csv file using csv.writer
    """
    output_data = generate_output_data(input_file)
    with open(output_file, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerows(output_data)


############################################################################
def main():
    process_input_and_export_output()


if __name__ == '__main__':
    main()
