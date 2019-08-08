import csv

f = open('alphabet_parameter.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
test = []
for line in rdr:
    test.append(line)

print(test[0][1])
f.close()