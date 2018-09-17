import csv

input_file = 'lyrics.csv'
output_file = 'lyrics-new.csv'

csv_input = open(input_file, 'rb')
csv_reader = csv.reader(csv_input)

csv_reader.next()
with open(output_file, 'wb') as csv_output:
    csv_writer = csv.writer(csv_output, delimiter=';', quoting=csv.QUOTE_ALL)
    for row in csv_reader:
        row[5] = row[5].replace('\n', ' ')
        csv_writer.writerow(row)
