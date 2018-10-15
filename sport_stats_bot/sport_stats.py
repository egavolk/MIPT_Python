import re
from bs4 import BeautifulSoup
import datetime
import requests

class Stats:
    def __init__(self):
        self.stats = dict()

    def UpdateStatsDict(self, date):
        now = datetime.datetime.now()
        if (self.stats.get(date) is not None) and (now.year != int(date[:4]) or
            now.month != int(date[5:7]) or now.day != int(date[8:])):
            return
        self.stats[date] = dict()
        requests.post('https://news.sportbox.ru/stats/' + date)
        response = requests.get('https://news.sportbox.ru/stats/' + date)
        html = response.text
        soup = BeautifulSoup(html)
        for i1 in range(20):
            cur_sport = soup.find_all(attrs={'id':'sport_{}'.format(i1)})
            if not cur_sport:
                continue
            cur_sport = str(cur_sport)
            sport_name = re.findall(r'<span>.*?</span>', cur_sport, re.DOTALL)[0][6:-7]
            self.stats[date][sport_name] = dict()
            sport_soup = BeautifulSoup(cur_sport)
            tournaments = sport_soup.find_all(attrs={'class':'col-lg-4 col-md-4 col-sm-6 col-xs-12'})
            for i2 in range(len(tournaments)):
                cur_soup = BeautifulSoup(str(tournaments[i2]))
                tournament_title = str(cur_soup.find_all(attrs={'class':'b-online__tour-title'}))
                tournament = str(re.findall(r'title[=]["].*?["]', tournament_title))[9:-3]
                if tournament:
                    tournament += '. '
                tournament1 = str(re.findall(r'<a.*?>.*?</a>', tournament_title, re.DOTALL))
                tournament1 = str(re.findall(r'>[^<]+?<', tournament1))
                j = 0
                while not tournament1[j].isupper():
                    j += 1
                tournament += tournament1[j:-36] + '. '
                tournament += str(re.findall(r'</a>.*?</div>', tournament_title, re.DOTALL))[7:-32] + '.'
                self.stats[date][sport_name][tournament] = dict()
                tournament_soup = BeautifulSoup(str(tournaments[i2]))
                games = tournament_soup.find_all(attrs={'class':'b-onlines-box__item'})
                for i3 in range(len(games)):
                    game_soup = BeautifulSoup(str(games[i3]))
                    
                    first_team = str(game_soup.find_all(attrs={'class':'b-onlines-box__side_left'}))
                    first_team = str(re.findall(r'<span[^>]*?>[^<]+?</span>', first_team, re.DOTALL))
                    first_team = str(re.findall(r'>.*?<', first_team, re.DOTALL))[3:-3]
                    
                    second_team = str(game_soup.find_all(attrs={'class':'b-onlines-box__side_right'}))
                    second_team = str(re.findall(r'<span[^>]*?>[^<]+?</span>', second_team, re.DOTALL))
                    second_team = str(re.findall(r'>.*?<', second_team, re.DOTALL))[3:-3]
                    
                    count = str(re.findall(r'class="count.*?>.*?</', str(games[i3]), re.DOTALL))
                    count = str(re.findall(r'>.*?<', count, re.DOTALL))[24:-14]
                    
                    comment = str(re.findall(r'class="b-onlines-box__comment.*?>.*?</', 
                                    str(games[i3]), re.DOTALL))
                    comment = str(re.findall(r'>.*?<', comment, re.DOTALL))[6:-3].strip()
                    if comment and comment[0] == '(' and comment[-1] == ')':
                        comment = comment[1:-1]
                    game = first_team
                    if count:
                        game += ' ' + count
                    if comment:
                        game += ' (' + comment + ')'
                    game += ' ' + second_team
                    
                    self.stats[date][sport_name][tournament][game] = { 'first_team':first_team, 'second_team':second_team,
                                                                 'count':count, 'comment':comment }
