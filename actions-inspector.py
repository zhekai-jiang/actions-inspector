import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument('--token', type = str, help = 'Your GitHub personal access token')
args = argParser.parse_args()

startDate = datetime(2024, 1, 20)
endDate = datetime(2024, 1, 26)
step = timedelta(hours = 6)
# Request in intervals of 6 hours to not reach the limit of 1000 entries per query
# It might have to be shortened if at some time there are more than 1000 runs in a 6-hour window

dates = []
numSuccessOnDate = {}
numFailureOnDate = {}
numTotalOnDate = {}

date = startDate
while date <= endDate:
    dates.append(date)

    numSuccessOnDate[date] = 0
    numFailureOnDate[date] = 0
    numTotalOnDate[date] = 0

    startTime = date # at 00:00:00

    endOfDay = date + timedelta(hours = 23, minutes = 59, seconds = 59)
    while startTime < endOfDay:
        endTime = min(startTime + step - timedelta(seconds = 1), endOfDay)

        page = 1
        while True:
            response = requests.get(
                url = 'https://api.github.com/repos/angular/angular/actions/runs',
                headers = {
                    'Accept': 'application/vnd.github+json',
                    'X-GitHub-Api-Version': '2022-11-28',
                    'Authorization': f'Bearer {args.token}'
                },
                params = {
                    'created': f'{startTime.isoformat()}Z..{endTime.isoformat()}Z', # UTC
                    'per_page': 100,
                    'page': page
                }
            )
            responseJson = response.json()

            totalCount = responseJson['total_count']

            print(f'{startTime} to {endTime}, {responseJson['total_count']} runs, page {page}')

            if totalCount > 1000:
                print('Please shorten time interval')
                exit(1)
                # A query can return a maximum of 1000 records as constrained by the API

            runs = responseJson['workflow_runs']
            if len(runs) == 0: # No more data
                break

            numTotalOnDate[date] += len(runs)
            numSuccessOnDate[date] += sum(1 for run in runs if run['conclusion'] == 'success')
            numFailureOnDate[date] += sum(1 for run in runs if run['conclusion'] == 'failure')
            
            if len(runs) < 100: # Current page is not full => no more pages
                break
            
            page += 1

        startTime += step
    
    date += timedelta(days = 1)

dateWithMostFailures = max(dates, key = lambda date: numFailureOnDate[date])
print(f'Date with most failing builds: {dateWithMostFailures.date()}, with {numFailureOnDate[dateWithMostFailures]} failing builds')

dateWithMostSuccesses = max(dates, key = lambda date: numSuccessOnDate[date])
print(f'Date with most successful builds: {dateWithMostSuccesses.date()}, with {numSuccessOnDate[dateWithMostSuccesses]} successful builds')

numsTotal = list(map(lambda date: numTotalOnDate[date], dates))
print(f'Frequency of Builds Received on Each Date: {numsTotal}')
plt.bar(dates, numsTotal)
plt.title('Frequency of Builds Received on Each Date')
plt.xlabel('Date')
plt.xticks(rotation = 30)
plt.subplots_adjust(bottom = 0.2)
plt.ylabel('Number of Builds')
plt.savefig('frequency-plot.pdf')
plt.show()
