#Import Libraries
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

#Variables for storing
teams=[]
pitchers=[]
pitchersPage=[]
df=[]
eras=[] 

PITCHER_NA = "Pitcher N/A"

Cities = [
    'Arizona',
    'Atlanta',
    'Baltimore',
    'Boston',
    'Chi Sox',
    'Chi Cubs',
    'Cincinnati',
    'Cleveland',
    'Colorado',
    'Detroit',
    'Houston',
    'Kansas City',
    'LA Angels',
    'LA Dodgers',
    'Miami',
    'Milwaukee',
    'Minnesota',
    'NY Yankees',
    'NY Mets',
    'Oakland',
    'Philadelphia',
    'Pittsburgh',
    'San Diego',
    'SF Giants',
    'Seattle',
    'St. Louis',
    'Tampa Bay',
    'Texas',
    'Toronto',
    'Washington',
]

Names = [
    "D'backs",
    'Braves',
    'Orioles',
    'Red Sox',
    'White Sox',
    'Cubs',
    'Reds',
    'Indians',
    'Rockies',
    'Tigers',
    'Astros',
    'Royals',
    'Angels',
    'Dodgers',
    'Marlins',
    'Brewers',
    'Twins',
    'Yankees',
    'Mets',
    'Athletics',
    'Phillies',
    'Pirates',
    'Padres',
    'Giants',
    'Mariners',
    'Cardinals',
    'Rays',
    'Rangers',
    'Blue Jays',
    'Nationals',
    ]

strikeOutsPerNine = []
pitcherWhip = []
def getSO22(url):
    so9 = ''
    pitcherUrl = url
    print(pitcherUrl + ' url')
    page = requests.get(pitcherUrl)
    soup = BeautifulSoup(page.text, 'html.parser')
    container = soup.find('tbody')
    for SOpernine in container.findAll('td', attrs={'class': 'right', 'data-stat': 'strikeouts_per_nine'}):
        #print(SOpernine.text)
        so9 = SOpernine.text
    return so9


#get all matchups for the day
def getMatchups():
    url = 'https://www.baseball-reference.com/previews/' #Website we're pulling from
    page = requests.get(url)
    matchups = BeautifulSoup(page.text, 'html.parser')

    #Get Teams
    for game in matchups.findAll('div', attrs={'class': 'game_summaries'}):
        for teams1 in game.findAll('table', attrs={'class': 'teams'}):
            for td in teams1.findAll('td', attrs={'class':None}):
                for teamName in td.find('a'):
                    teams.append(teamName) #appends team names to list 'teams'
    #Get Pitchers, ERAs, SO/9, WHIP            
        for pitchers1 in game.findAll('table', attrs={'class': None}):
            count = 0
            for tr in pitchers1.findAll('tr', attrs={'class': None}):
                count += 1
            for td2 in pitchers1.findAll('td', attrs={'class': None}):
                for pitcherName in td2.findAll('a'):
                    if(count < 2 ):
                        #TODO: Make another function to do this!
                        pitchers.append(PITCHER_NA)
                        pitchers.append(PITCHER_NA)
                        eras.append(PITCHER_NA)
                        eras.append(PITCHER_NA)
                        strikeOutsPerNine.append(PITCHER_NA)
                        strikeOutsPerNine.append(PITCHER_NA)
                        pitcherWhip.append(PITCHER_NA)
                        pitcherWhip.append(PITCHER_NA)
                    else:
                        p = pitcherName.text
                        print(p)
                        pitchers.append(p) #appends pitcher names to list 'pitchers'

                        def getSO(url):
                            if(url != ''):
                                so9 = ''
                                whip = ''
                                pitcherUrl = url
                                #print(pitcherUrl + ' url')
                                page = requests.get(pitcherUrl)
                                soup2 = BeautifulSoup(page.text, 'html.parser')
                                container = soup2.find('tr', attrs={'id': 'pitching_standard.2020'})
                                #print(container)
                                for SOpernine in container.findAll('td', attrs={'class': 'right', 'data-stat': 'strikeouts_per_nine'}):
                                    print(SOpernine.text)
                                    so9 = SOpernine.text
                                for Pwhip in container.findAll('td', attrs={'class': 'right', 'data-stat': 'whip'}):
                                    print(Pwhip.text)
                                    whip = Pwhip.text
                                return so9, whip
                            else:
                                return ("N/A")
                    
                        strikes, whip = (getSO(pitcherName['href']))
                        strikeOutsPerNine.append(strikes)
                        pitcherWhip.append(whip)
                        #GET ERAS
                        es = pitcherName.next_sibling.next_sibling  #this gets pitcher's number, age, handed, record, era
                        #print(es) 
                        split_es = es.split(', ') #split that one string into multiple strings

                        if(split_es[3] == ''):
                            era = "MLB Debut"
                        else:
                            era = split_es[4]

                        finalE = era.replace(')', '')
                        eras.append(finalE) #append ERA to list
                        
getMatchups()

df = pd.DataFrame()
df['Team'] = teams
df['Pitcher'] = pitchers
df['ERA'] = eras
df['S/O 9'] = strikeOutsPerNine
df['Whip'] = pitcherWhip
print(df)
df.to_csv('/Users/nickostendorf/ndorf/Tech/Python/MLBStarters/MLBteams.csv')
citiesteams = pd.DataFrame()
citiesteams['City'] = Cities
citiesteams['Names'] = Names
citiesteams.to_csv('/Users/nickostendorf/ndorf/Tech/Python/MLBStarters/MLB.csv')

#Get Starting Pitcher that has been requested from GUI
def getStartingPitchers(team1):

    locRow1 = df.loc[df['Team'] == team1]
    rowNum1 = locRow1.index.tolist()[0]
    getPitcher1 = df.loc[rowNum1, 'Pitcher']
    getERA1 = df.loc[rowNum1, 'ERA']
    
    return(getPitcher1 + '\n ' + getERA1)

#Switching team names... Should most likely do this beforehand to save time
def changeTeams(team1):
    locTeam = citiesteams.loc[citiesteams['City'] == team1]
    rowTeam = locTeam.index.tolist()[0]
    getName = citiesteams.loc[rowTeam, 'Names']

    return(getStartingPitchers(getName))