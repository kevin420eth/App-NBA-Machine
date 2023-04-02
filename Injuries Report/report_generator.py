import requests
from datetime import datetime
from bs4 import BeautifulSoup


url = "https://www.espn.com/nba/injuries"

response = requests.get(url)

content = response.text

soup = BeautifulSoup(content,"lxml")

injuries_dict ={}

all_injuries_table = soup.find_all("div", class_="ResponsiveTable Table__league-injuries")

for each_team in all_injuries_table:
    team_name = each_team.find("span",class_="injuries__teamName ml2").text
    injuries_dict[team_name] = []

    all_injuries_player = each_team.find_all("tr", class_="Table__TR Table__TR--sm Table__even")
    
    for _ in all_injuries_player:
        player_name = _.find("a",class_="AnchorLink").text
        position = _.find("td",class_="col-pos Table__TD").text
        status = _.find("td",class_="col-stat Table__TD").find("span").text
        description = _.find("td",class_="col-desc Table__TD").text
        injuries_dict[team_name].append({"name":player_name,"position":position,"status":status,"description":description})

    # print(f"{team_name}\n{player_name} {position} {status}\n{description}")


# search_team = input("Please Enter The Team Name: ")

# for _ in injuries_dict[search_team]:

#     print(f'\n{_["position"]} | {_["name"]} - {_["status"]}\n{_["description"]}\n')




today_date = str(datetime.now())

today_date = today_date.split()[0].replace("-","")

url = f"https://www.espn.com/nba/scoreboard/_/date/{today_date}"

response = requests.get(url)

content = response.text

soup = BeautifulSoup(content,"lxml")

nba_scooreboard = soup.find_all(name="a", class_="AnchorLink Button Button--sm Button--anchorLink Button--alt mb4 w-100 mr2")

game_link =[]

for x in nba_scooreboard:
    if x.text =="Gamecast":
        game_link.append(x["href"])

tomorrow_match_team = []

for each_game_link in game_link:
    each_game_page = f"https://www.espn.com{each_game_link}"
    response = requests.get(each_game_page)
    content = response.text
    soup = BeautifulSoup(content,"lxml")
    match_team = soup.find_all(name="div",class_="ScoreCell__TeamName ScoreCell__TeamName--displayName truncate db")
    score_table = soup.find_all(name="td", class_="Table__TD")
    ot_dectector = soup.find_all(name="th", class_="Table__TH" )
    date_section = soup.find(name="div", class_="n8 GameInfo__Meta")
    game_date = date_section.find(name="span").text
    

    away_team = match_team[0].text
    home_team = match_team[1].text
    tomorrow_match_team.append(away_team)
    tomorrow_match_team.append(home_team)

with open(f"Injuries Report/Injuries Report - {today_date}.txt", "w") as f:
    for _ in tomorrow_match_team:
        f.write(f"--------------------{_}--------------------\n")

        try:
            for __ in injuries_dict[_]:
                f.write(f'\n{__["position"]} | {__["name"]} - {__["status"]}\n{__["description"]}\n\n')
        except KeyError:
            f.write("\nNo Injuries\n\n")

print("\nReport is completed!\n")
