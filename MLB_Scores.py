#Imports
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

#Variables
teams=[] #List to store team names
points=[] #List to store all points
d=[] #List to append data to create data frame
url = 'https://www.teamrankings.com/mlb/stat/runs-per-game' #Website we're pulling data from 
#url to pull data for 1st 5 innings
#url = 'https://www.teamrankings.com/mlb/stat/first-5-innings-runs-per-game' 
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
container = soup.find('tbody')

#LOOP FOR TEAMS AND SCORES
for row in container.findAll('tr'):
	for team in row.findAll('td', attrs={"class": "text-left nowrap"}):
		for a in team.find('a'): #this pulls teams name
			teams.append(a)
		pa = [] #list for points
		for score in row.findAll('td', attrs={"class": "text-right"}): #gets avg score and home score: points[0]=avg, points[3]=home, points[4]=away
			p = score.text
			points.append(p)
			pa.append(p)
		d.append({'Team': a, '2020': pa[0], 'Last 3': pa[1], 'Last 1': pa[2], 'Home': pa[3], 'Away': pa[4]})
df = pd.DataFrame(d, columns = ['Team', '2020', 'Last 3', 'Last 1', 'Home', 'Away'])

#Gets points of each team from data frame and adds together, returns sum
def get2019(team1, team2):
	locRow1 = df.loc[df['Team'] == team1]
	rowNum1 = locRow1.index.tolist()[0]
	getAvg1 = df.loc[rowNum1, '2020']
	fltAvg1 = float(getAvg1)
	rndAvg1 = round(fltAvg1, 2)

	locRow2 = df.loc[df['Team'] == team2]
	rowNum2 = locRow2.index.tolist()[0]
	getAvg2 = df.loc[rowNum2, '2020']
	fltAvg2 = float(getAvg2)
	rndAvg2 = round(fltAvg2, 2)

	return(rndAvg1 + rndAvg2)

#Gets Away/Home team points from data fram and adds together, returns sum
def getHA(team1, team2):
	locRow1 = df.loc[df['Team'] == team1]
	rowNum1 = locRow1.index.tolist()[0]
	getAway = df.loc[rowNum1, 'Away']
	fltAvg1 = float(getAway)
	rndAvg1 = round(fltAvg1, 2)

	locRow2 = df.loc[df['Team'] == team2]
	rowNum2 = locRow2.index.tolist()[0]
	getHome = df.loc[rowNum2, 'Home']
	fltAvg2 = float(getHome)
	rndAvg2 = round(fltAvg2, 2)

	return(rndAvg1 + rndAvg2)