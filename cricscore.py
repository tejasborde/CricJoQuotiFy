import os
import requests
from datetime import datetime



class ScoreGet:
  def __init__(self):
    self.url_get_all_matches =os.getenv('url_get_all_matches')
    self.url_get_score = os.getenv('url_get_score')
    self.api_key =os.getenv('api_key')
    self.unique_id = ""  # unique to every match
    self.id_list = []
    self.results = {}


  
  def get_unique_id_and_results(self):
    permiter = {"apikey": self.api_key}
    resp = requests.get(self.url_get_all_matches, params=permiter)
    resp_dict = resp.json()
    f = 0
    for i in resp_dict['matches']:
        if (i['matchStarted']):
            todays_date = datetime.today().strftime('%Y-%m-%d')

            if todays_date == i['date'].split("T")[0]:
              try:
                if(i['toss_winner_team']!="no toss"):
                  f = 1
                  self.id_list.append(i['unique_id'])
              except KeyError:
                pass
    if not f:
        self.unique_id = -1
    for i in self.id_list:
        self.unique_id = i
        data = self.get_score(i)
        self.results[self.unique_id] = data

    return self.results

  


  def get_score(self,unique_id):
    data=""
    if(unique_id == -1):
      data = "No live matches today"
    else:
      permiter = {"apikey": self.api_key, "unique_id": self.unique_id}
      resp = requests.get(self.url_get_score, params=permiter)
      data = resp.json()
      try:
        data = "Match Id : " + str(self.unique_id) + "\n" + data['score']
      except KeyError:
        data= "Match Id : " + str(self.unique_id) + "\n"+"Scores Not Available."
    return data

def detailed_scorecard(id):
	url_matches = os.getenv('url_get_all_matches')
	url_scorecard = os.getenv('fantasy_summary')
	url_get_score =  os.getenv('url_get_score')
	api_key = os.getenv('api_key')
	unique_id = id
	scorecard_deatils = {}
	permiter = {"apikey": api_key, "unique_id": unique_id}
	scorecard = requests.get(url_scorecard, params=permiter)
	scorecard = scorecard.json()
	match_deatils = requests.get(url_matches, params={"apikey": api_key})
	match_deatils = match_deatils.json()
	scorecard_deatils["toss-win"] = scorecard["data"]["toss_winner_team"]
	scores = requests.get(url_get_score, params=permiter)
	scores = scores.json()
	match_live_data = "Match Id : " + str(unique_id) + "\n" + scores['score']
	scorecard_deatils["match"] = match_live_data
	bt1 = "\n"
	try:
		battingt1 = scorecard['data']['batting'][0]['scores']
		count = 1
		for t1 in battingt1:
			bt1 = bt1 + "\n**" + str(count) + ")" + (
			    (t1["batsman"]+"**").ljust(20) + "\n" + "R:" + str(t1["R"]) +
			    " B:" + str(t1["B"]) + " 4:" + str(t1["4s"]) + " 6:" +
			    str(t1["6s"]) + " SR:" +
			    str(t1["SR"])).ljust(50) + "\n" +"**"+t1["dismissal-info"]+"**"
			count = count + 1
	except IndexError:
		pass

	bt2 = "\n"
	try:
		bowlingt1 = scorecard["data"]["bowling"][0]["scores"]
		count = 1
		for t1 in bowlingt1:
			bt2 = bt2 + "\n**" + str(count) + ")" + (
			    (t1["bowler"]+"**").ljust(20) + "\n" + "O:" + str(t1["O"]) + " M:" +
			    str(t1["M"]) + " R:" + str(t1["R"]) + " W:" + str(t1["W"]) +
			    " Eco:" + str(t1["Econ"])).ljust(50)
			count = count + 1
	except IndexError:
		pass

	scorecard_deatils["1-innings"] = bt1 + "\n" + bt2

	bt1 = "\n"
	try:
		battingt2 = scorecard['data']['batting'][1]['scores']
		count = 1
		for t1 in battingt2:
			bt1 = bt1 + "\n**" + str(count) + ")" + (
			    (t1["batsman"]+"**").ljust(20) + "\n" + "R:" + str(t1["R"]) +
			    " B:" + str(t1["B"]) + " 4:" + str(t1["4s"]) + " 6:" +
			    str(t1["6s"]) + " SR:" +
			    str(t1["SR"])).ljust(50) + "\n" + "**"+t1["dismissal-info"]+"**"
			count = count + 1
	except IndexError:
		pass

	bt2 = "\n"
	try:
		count = 1
		bowlingt2 = scorecard["data"]["bowling"][1]["scores"]
		for t1 in bowlingt2:
			bt2 = bt2 + "\n**" + str(count) + ")" + (
			    (t1["bowler"]+"**").ljust(20) + "\n" + "O:" + str(t1["O"]) + " M:" +
			    str(t1["M"]) + " R:" + str(t1["R"]) + " W:" + str(t1["W"]) +
			    " Eco:" + str(t1["Econ"])).ljust(50)
			count = count + 1
	except IndexError:
		pass
	scorecard_deatils["2-innings"] = bt1 + "\n" + bt2
	return scorecard_deatils
