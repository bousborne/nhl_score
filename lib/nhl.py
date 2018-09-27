import requests
import datetime

# https://gitlab.com/dword4/nhlapi/blob/master
NHL_API_URL = "http://statsapi.web.nhl.com/api/v1/"
NHL_URL = "http://statsapi.web.nhl.com"
OVECHKIN = "https://statsapi.web.nhl.com/api/v1/people/8471214"

def get_teams():
    """ Function to get a list of all the teams name"""

    url = '{0}/teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teams = []

    for team in results['teams']:
        teams.append(team['franchise']['teamName'])

    return teams


def get_team_id(team_name):
    """ Function to get team of user and return NHL team ID"""

    url = '{0}/teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teams = []

    for team in results['teams']:
        if team['franchise']['teamName'] == team_name:
            return team['id']

    raise Exception("Could not find ID for team {0}".format(team_name))


def fetch_score(team_id):
    """ Function to get the score of the game depending on the chosen team.
    Inputs the team ID and returns the score found on web. """

    # Get current time
    now = datetime.datetime.now()

    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    print('fetch score url:', url)
    # Avoid request errors (might still not catch errors)
    try:
        score = requests.get(url)
        score = score.json()
        #import pdb; pdb.set_trace();
        if int(team_id) == int(score['dates'][0]['games'][0]['teams']['home']['team']['id']):
            score = int(score['dates'][0]['games'][0]['teams']['home']['score'])
        else:
            score = int(score['dates'][0]['games'][0]['teams']['away']['score'])
        fetch_goal_scorer(url, score)
        # Print score for test
        print("Score: {0} Time: {1}:{2}:{3}".format(score, now.hour, now.minute, now.second))
        return score
    except requests.exceptions.RequestException:
        print("Error encountered, returning 0 for score")
        return 0

def fetch_goal_scorer(game_url, score):
    """ Function to determine who scored last goal. """
    scorer = None

    live_link = requests.get(game_url).json()['dates'][0]['games'][0]['link']
    live_url = '{0}{1}'.format(NHL_URL, live_link)
    liveFeed = requests.get(live_url).json()
    #import pdb; pdb.set_trace();
    if score > 0:
        playNumber = int(liveFeed['liveData']['plays']['scoringPlays'][score-1])
        scorer = liveFeed['liveData']['plays']['allPlays'][playNumber]['players'][0]['player']['fullName']

    return scorer

def check_season():
    """ Function to check if in season. Returns True if in season, False in off season. """
    # Get current time
    now = datetime.datetime.now()
    if now.month in (7, 8):
        return False
    else:
        return True


def check_if_game(team_id):
    """ Function to check if there is a game now with chosen team. Returns True if game, False if NO game. """

    
    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id) #Only shows games after noon, so will sleep till 12:10 pm
    try:
        gameday_url = requests.get(url)
        if "gamePk" in gameday_url.text:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        # Return True to allow for another pass for test
        print("Error encountered, returning True for check_game")
        return True

      
def check_game_end(team_id):
    """ Function to check if the game ofchosen team is over. Returns True if game, False if NO game. """

    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    # Avoid request errors
    try:
        game_status = requests.get(url)
        game_status = game_status.json()
        game_status = int(game_status['dates'][0]['games'][0]['status']['statusCode'])
        if game_status == 7:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        # Return False to allow for another pass for test
        print("Error encountered, returning False for check_game_end")
        return False


def check_ovechkin_season_goals():

    url = '{0}/stats?stats=statsSingleSeason&season=20172018'.format(OVECHKIN)
    #import pdb; pdb.set_trace();
    try:
        goals = requests.get(url)
        goals = goals.json()
        goals = goals['stats'][0]['splits'][0]['stat']['goals']
        return goals
    except requests.exceptions.RequestException:
        # Return False to allow for another pass for test
        print("Error encountered, returning False for check_game_end")
        return False

# Returns number of goals ovechkin is on pace for in 2017-2018 season. Must be in season to work.
def check_ovechkin_on_pace_regular_season_goals():
    url = '{0}/stats?stats=onPaceRegularSeason&season=20172018'.format(OVECHKIN)
        #import pdb; pdb.set_trace();
    try:
        goals = requests.get(url)
        goals = goals.json()
        goals = goals['stats'][0]['splits'][0]['stat']['goals']
        return goals
    except requests.exceptions.RequestException:
        # Return False to allow for another pass for test
        print("Error encountered, returning False")
        return False

def check_ovechkin_career_goals():
    import datetime

    if datetime.datetime.today().month > 6:
        season_year_end = datetime.datetime.today().year + 1
        season_year_begin = datetime.datetime.today().year
    else:
        season_year_end = datetime.datetime.today().year
        season_year_begin = datetime.datetime.today().year - 1

    print(season_year_end);
    print(season_year_begin);
    import pdb; pdb.set_trace();
    while season_year_begin >= 2004:
        curr_season_modifier = str(season_year_begin) + (str(season_year_end))
        print(curr_season_modifier)
        url = '{0}/stats?stats=onPaceRegularSeason&season={1}'.format(OVECHKIN, curr_season_modifier)

        try:
            goals = requests.get(url)
            goals = goals.json()
            goals = goals['stats'][0]['splits'][0]['stat']['goals']

            print(curr_season_modifier, goals)
        except requests.exceptions.RequestException:
            # Return False to allow for another pass for test
            print("Error encountered, returning False")
            return False
        --season_year_begin
        career_goals = career_goals + goals

    return goals
