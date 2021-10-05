#Script that takes in CSV files from /csv_files directory, parses them, then deletes them
import os
import csv
import datetime
import codecs
import shutil
from flask import abort

def calcuate_roas(conversion_value, cost):
    #Calcuate Return On Ad Spend (ROAS)
    try:
        return float(conversion_value) / float(cost)
    except:
        return False

def main():
    #Check if directory has files in it
    if not os.listdir('./csv_files'):
        abort(400, "No files in directory")

    for item in os.listdir('./csv_files'):
        #Loop through each file in the directory
        #Using codecs because of encoding issues
        file = csv.reader(codecs.open('./csv_files/{0}'.format(item), 'rU', 'utf-16'), delimiter='\t')

        #Get the currency for the filename
        for index, row in enumerate(file):
            currency = row[6]
            if index == 1:
                break

        #Create the file with the headers
        file_datetime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        try:
            os.makedirs(os.path.dirname('processed\{0}\search_terms'.format(currency)))
        except:
            pass
        header = ['search_term', 'clicks', 'cost', 'impressions', 'conversion_value', 'roas']
        f = open('processed\{0}\search_terms\{1}.csv'.format(currency,file_datetime), 'w')
        writer = csv.writer(f)
        writer.writerow(header)

        current_row = 0
        for row in file:
            #Loop through each row in the csv and calcuate the ROAS
            try:
                roas_cost = calcuate_roas(row[10], row[7])
                if roas_cost is False:
                    continue
            except UnicodeError as e:
                pass

            #Build the data list and insert it to the csv
            data = [row[0], row[5], row[7], row[8], row[9], roas_cost]
            try:
                writer.writerow(data)
            except UnicodeError:
                pass

            current_row += 1
        f.close()
        print("Finshed")

if __name__ == "__main__":
    # execute only if run as a script
    main()
