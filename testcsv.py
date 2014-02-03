import csv

def convertToCSV(valuescrawled):
		valuescsv = csv.writer(open('values.csv', 'wb'), delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for values in valuescrawled:
			valuescsv.writerow(values)

valuescrawled = [ ["hi",'bye','seven'] , ["hi",'bye','seven'] ,  ["hi",'bye','seven'] ,  ]
convertToCSV(valuescrawled)			