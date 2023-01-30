import requests
import datetime
import sys

facilities = ['rpac', 'jos', 'nrc']

def normal():
    for facility in facilities:
        summ = 0
        url = f"https://recsports.osu.edu/fms/Home/GetLocations?locationCode={facility}"

        r = requests.get(url)

        for location in r.json()['locations']:
            summ += int(location['lastCount'])

        with open(f'data/{facility}/{facility}_today.csv', 'a') as f:
            f.write(f"{summ},")

def daily():
    now = datetime.datetime.today()
    dow = now.weekday()
    print(dow)
    for facility in facilities:
        with open(f'data/{facility}/{facility}_today.csv', 'r+') as f1:
            line = now.strftime("%Y-%m-%d,") + f1.read()
            f1.seek(0)
            f1.truncate()
            # Move today's line to the full file
            with open(f'data/{facility}/{facility}.csv', 'a') as f2:
                f2.write("\n")
                f2.write(line)
            """
            # Caclulate the new averages
            with open(f'data/{facility}/{facility}_avg.csv', 'r+') as f3:
                lines = f3.readlines()
                # Get the current average
                avg_data = [float(i) for i in lines[dow].split(',')]
                # Get weight from end of avgs string
                weight = avg_data.pop()
                new_data = [float(i) for i in line.split(',')]
                new_avgs = [(a * weight + b) / (weight + 1) for a, b in zip(avg_data, new_data)]
                lines[dow] = ','.join(map(str, new_avgs)) + ',' + str(weight + 1) + '\n'
                f3.write(''.join(lines))
            """


if __name__ == '__main__':
    if len(sys.argv) < 2:
        normal()
    elif sys.argv[1] == 'daily':
        daily()
