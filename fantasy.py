# Import libraries
import requests
import urllib.request
import time
import xlsxwriter
from bs4 import BeautifulSoup

# Create a dictionary for Player Rankings
RBs = {}
WRs = {}
QBs = {}
TEs = {}
Ks = {}
D = {}
position_dict = [RBs, WRs, QBs, TEs, Ks, D]

def create_player(dct, player_name, place):
    """
    Create a player in the dictionary with and fill 
    """
    dct.update({player_name: ['N/A'] * place})
    
def update_player_rank(dct, player_name, place, rank):
    """
    update a player's rank based on where the place is
    """
    dct.get(player_name)[place - 1] = rank
    

positions = ['RB', 'WR', 'QB','TE', 'K', 'D']
websites = 1

#_____________________________WalterFootball____________________________________
WalterFootball = ['runningbacks','runningbacks_2','runningbacks_3',
'widereceivers', 'widereceivers_2', 'widereceivers_3', 'widereceivers_4',
'quarterbacks','quarterbacks_2','quarterbacks_3','tightends','tightends_2','tightends_3']

print('----------WalterFootball.com----------')

Rank = 1
position_counter = 0
for link in WalterFootball:
    if '_' not in link:
        print('--' + positions[position_counter] + '--')
        position_counter += 1 
        Rank = 1
    # Set the URL you want to webscrape from
    url = 'https://walterfootball.com/fantasy2020' + link + '.php'
    # Connect to the URL
    response = requests.get(url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    for one_b_tag in soup.findAll('b'):
        Name = one_b_tag.get_text()
        if 'Bye' in Name:
            pName = ''
            if Name.split(',')[0].split(' ')[2] == '':
                pName = Name.split(',')[0].split(' ')[3] + ' ' + Name.split(',')[0].split(' ')[4]
            else:
                pName = Name.split(',')[0].split(' ')[2] + ' ' + Name.split(',')[0].split(' ')[3]
            create_player(position_dict[position_counter - 1], pName, websites)
            update_player_rank(position_dict[position_counter - 1], pName, websites, Rank)    
            Rank += 1       

#_____________________________FantasyPros____________________________________
FantasyPros = ['rb','wr', 'qb', 'te', 'k']

print('----------FantasyPros.com----------')
websites = 2
position_counter = 0
for link in FantasyPros:
    Rank = 1
    print('--' + positions[position_counter] + '--')
    # Set the URL you want to webscrape from
    url = 'https://www.fantasypros.com/nfl/rankings/'+ link +'-cheatsheets.php'
    # Connect to the URL
    response = requests.get(url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    counter = 0
    for one_a_tag in soup.findAll('span',class_="full-name"):
        pName = one_a_tag.get_text()
        if pName not in position_dict[position_counter]:
            create_player(position_dict[position_counter], pName, websites)
            update_player_rank(position_dict[position_counter], pName, websites, Rank)
        else:
            position_dict[position_counter].get(pName).append(Rank)
        Rank += 1
    #update unlisted players
    for key in position_dict[position_counter]:
        if len(position_dict[position_counter].get(key)) != websites:
            position_dict[position_counter].get(key).append('N/A')
    position_counter += 1    

#_____________________________FantasyFootballCalculator____________________________________
FFC = ['running-back','wide-receiver', 'quarterback', 'tight-end', 'kicker', 'team-defense-dst']

print('----------FantasyFootballCalculator.com----------')
websites = 3
position_counter = 0
for link in FFC:
    Rank = 1
    print('--' + positions[position_counter] + '--')
    # Set the URL you want to webscrape from
    url = 'https://fantasyfootballcalculator.com/rankings/ppr/'+ link
    # Connect to the URL
    response = requests.get(url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    counter = 0
    for one_a_tag in soup.findAll('td',class_="rankings-player-name"):
        pName = one_a_tag.get_text()
        if pName not in position_dict[position_counter]:
            create_player(position_dict[position_counter], pName, websites)
            update_player_rank(position_dict[position_counter], pName, websites, Rank)
        else:
            position_dict[position_counter].get(pName).append(Rank)
        #print(str(Rank) + ' ' + one_a_tag.get_text())
        Rank += 1
        #update unlisted players
    for key in position_dict[position_counter]:
        if len(position_dict[position_counter].get(key)) != websites:
            position_dict[position_counter].get(key).append('N/A')    
    position_counter += 1

#_____________________________lineups.com____________________________________
lineups = ['running-back-rb','wide-receiver-wr', 'quarterback-qb', 'tight-end-te', 'kicker-k', 'defense']

print('----------lineups.com----------')
websites = 4
position_counter = 0
for link in lineups:
    Rank = 1
    print('--' + positions[position_counter] + '--')
    # Set the URL you want to webscrape from
    url = 'https://www.lineups.com/fantasy-football-rankings/'+ link
    # Connect to the URL
    response = requests.get(url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    counter = 0
    for one_a_tag in soup.findAll('a',class_="link-black-underline"):
        for temp in one_a_tag.findAll('span',class_=""):
            if temp.get_text().split(" ")[0][0] != "\n":    
                pName = temp.get_text()
                if pName not in position_dict[position_counter]:
                    create_player(position_dict[position_counter], pName, websites)
                    update_player_rank(position_dict[position_counter], pName, websites, Rank)
                else:
                    position_dict[position_counter].get(pName).append(Rank)
                Rank += 1
    #update unlisted players
    for key in position_dict[position_counter]:
        if len(position_dict[position_counter].get(key)) != websites:
            position_dict[position_counter].get(key).append('N/A')
            
    position_counter += 1

#_____________________________fantasyData.com____________________________________
fantasyData = ['rb','wr', 'qb', 'te', 'k', 'dst']

print('----------fantasyData.com----------')
websites = 5
position_counter = 0
for link in fantasyData:
    Rank = 1
    print('--' + positions[position_counter] + '--')
    # Set the URL you want to webscrape from
    url = 'https://fantasydata.com/nfl/'+ link+ '-rankings'
    # Connect to the URL
    response = requests.get(url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    counter = 0
    for one_a_tag in soup.findAll('td'):
        #print(one_a_tag.get_text().split(' ')[0][1:] + ' ' + one_a_tag.get_text().split(' ')[1])        
        pName = one_a_tag.get_text().split(' ')[0][1:] + ' ' + one_a_tag.get_text().split(' ')[1]
        if pName not in position_dict[position_counter]:
            create_player(position_dict[position_counter], pName, websites)
            update_player_rank(position_dict[position_counter], pName, websites, Rank)
        else:
            position_dict[position_counter].get(pName).append(Rank)
        Rank += 1
    #update unlisted players
    for key in position_dict[position_counter]:
        if len(position_dict[position_counter].get(key)) != websites:
            position_dict[position_counter].get(key).append('N/A')       
    position_counter += 1


######-------------------------------------------------------------------------
#Write to an excel file
    
workbook = xlsxwriter.Workbook('/Users/AalanMohammad/Desktop/FantasyRankings2020.xlsx')

for pos in range(len(positions)): 
    worksheet = workbook.add_worksheet(positions[pos])
    row = 1
    col = 0
    worksheet.write(0, 0, "Name")
    worksheet.write(0, 1, "WalterFootball")
    worksheet.write(0, 2, "FantasyPros")
    worksheet.write(0, 3, "FantasyFootballCalculators")
    worksheet.write(0, 4, "lineups")
    worksheet.write(0, 5, "FantasyData")
    for name in position_dict[pos]:
        worksheet.write(row, col, name)
        worksheet.write(row, col + 1, position_dict[pos].get(name)[0])
        worksheet.write(row, col + 2, position_dict[pos].get(name)[1])
        worksheet.write(row, col + 3, position_dict[pos].get(name)[2])
        worksheet.write(row, col + 4, position_dict[pos].get(name)[3])
        worksheet.write(row, col + 5, position_dict[pos].get(name)[4])
        row += 1
workbook.close()


