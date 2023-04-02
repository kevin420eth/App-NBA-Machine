import encodings, requests
from gettext import find
from bs4 import BeautifulSoup
from datetime import timedelta, date

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

start_dt = date(2013,2,20)
end_dt = date(2013,2,22)

date_list =[]

for dt in daterange(start_dt, end_dt):
    date_list.append(dt.strftime("%Y%m%d"))



for each_day in date_list:

    url = f"https://www.espn.com/nba/scoreboard/_/date/{each_day}"

    response = requests.get(url)

    content = response.text

    soup = BeautifulSoup(content,"lxml")

    nba_scooreboard = soup.find_all(name="a", class_="AnchorLink Button Button--sm Button--anchorLink Button--alt mb4 w-100 mr2")

    game_link =[]

    for x in nba_scooreboard:
        if x.text =="Gamecast":
            game_link.append(x["href"])

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

        if ot_dectector[5].text=="OT":
            away_team_1q = score_table[1].text
            away_team_2q = score_table[2].text
            away_team_3q = score_table[3].text
            away_team_4q = score_table[4].text
            away_team_ot = score_table[5].text

            home_team_1q = score_table[8].text
            home_team_2q = score_table[9].text
            home_team_3q = score_table[10].text
            home_team_4q = score_table[11].text
            home_team_ot = score_table[12].text
        else:
            away_team_1q = score_table[1].text
            away_team_2q = score_table[2].text
            away_team_3q = score_table[3].text
            away_team_4q = score_table[4].text
            away_team_ot = 0

            home_team_1q = score_table[7].text
            home_team_2q = score_table[8].text
            home_team_3q = score_table[9].text
            home_team_4q = score_table[10].text
            home_team_ot = 0

        # print(f"{away_team} VS {home_team} {game_date}")
        # print(f"{away_team_1q} {away_team_2q} {away_team_3q} {away_team_4q} {away_team_ot}")
        # print(f"{home_team_1q} {home_team_2q} {home_team_3q} {home_team_4q} {home_team_ot}")

        with open("Game History Data/2012-2013 Regular Season.csv", "a") as f:
            f.write(f"{game_date},{away_team},{away_team_1q},{away_team_2q},{away_team_3q},{away_team_4q},{away_team_ot},{home_team},{home_team_1q},{home_team_2q},{home_team_3q},{home_team_4q},{home_team_ot}\n")

    print(f"{each_day} is completed")