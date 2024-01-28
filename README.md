# Inspection of GitHub Actions Distribution in the Angular Repository

## To Run the Script

The script can be executed from the command line using
```
python actions-inspector.py --token <your GitHub personal access token>
```

It requires a GitHub personal access token with access to Actions, so that we can make a sufficient number of API calls to fetch all data without reaching the rate limit imposed by GitHub API, which is very low for unauthenticated users. It can be created [here](https://github.com/settings/tokens).


The script also uses some libraries such as `requests` and `matplotlib`. If they are not available in the system, you can install them using
```
pip install <library needed>
```

It will take some time for the script to run. It will show its progress by printing the time range and number of page it is currently querying.

At the end, the program will print to the console (a) the date with the most failing builds, (b) the date with the most successful builds, and (c) the frequency of builds received on each of the 7 days. It will also show the plot of the frequency and save it in the file `frequency-plot.pdf`.

## Customization

### Date Range

Currently, this script fetches builds from January 20 to 26, 2024 only. If you wish to change the time range, please modify [`startDate` on line 10](https://github.com/zhekai-jiang/actions-inspector/blob/fea1a25eba7cee69abb0100870e07ab02fc4617e/actions-inspector.py#L10) and [`endDate` on line 11](https://github.com/zhekai-jiang/actions-inspector/blob/fea1a25eba7cee69abb0100870e07ab02fc4617e/actions-inspector.py#L11) of the source code. Note that each date is defined in UTC time (0:00 to 23:59 UTC).

### Query Interval

This script queries in intervals of 6 hours, in order to not reach the limit of 1000 entries per query. It might have to be shortened if at some time there are more than 1000 runs in a 6-hour window. This can be customized by modifying [`step` on line 12](https://github.com/zhekai-jiang/actions-inspector/blob/fea1a25eba7cee69abb0100870e07ab02fc4617e/actions-inspector.py#L12) of the source code.
