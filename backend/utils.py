import statistics as st
import numbers


''' CLASES '''

class Statistics:
    def __init__(self,
                 mean,
                 median,
                 mode,
                 stdev,
                 variance):
        self._mean = mean,
        self._median = median
        self._mode = mode
        self._stdev = stdev
        self._variance = variance
        
    @property
    def mean(self):
        return self._mean
    
    @property
    def median(self):
        return self._median
    
    @property
    def mode(self):
        return self._mode
    
    @property
    def stdev(self):
        return self._stdev
    
    @property
    def mean(self):
        return self._mean


class SeasonStats:
    def __init__(self,
                 events_list,
                 events_number,
                 events_player_list,
                 events_player_number,
                 events_player_rate,
                 events_team_list,
                 events_team_number,
                 events_team_rate,
                 tournaments_list,
                 tournaments_number,
                 torunaments_rate,
                 leagues_list,
                 leagues_number,
                 leagues_rate,
                 duels_list,
                 duels_number,
                 duels_average,
                 duels_stdev,
                 combats_list,
                 combats_numbers,
                 combats_average,
                 combats_stdev,
                 rounds_number,
                 rounds_average,
                 rounds_stdev,
                 players_list,
                 players_number,
                 players_average,
                 players_stdev,
                 teams_list,
                 teams_number,
                 teams_average,
                 teams_stdev,
                 characters_list,
                 characters_number,
                 characters_average,
                 characters_stdev,
                 players_characters_list,
                 players_characters_number,
                 players_characters_average,
                 players_characters_stdev,
                 winners_player_list,
                 winners_player_number,
                 winners_team_list,
                 winners_team_number):
        self.events_list = events_list
        self.events_number = events_number
        self.events_player_list = events_player_list
        self.events_player_number = events_player_number
        self.events_player_rate = events_player_rate
        self.events_team_list = events_team_list
        self.events_team_number = events_team_number
        self.events_team_rate = events_team_rate
        self.tournaments_list = tournaments_list
        self.tournaments_number = tournaments_number
        self.torunaments_rate = torunaments_rate
        self.leagues_list = leagues_list
        self.leagues_number = leagues_number
        self.leagues_rate = leagues_rate
        self.duels_list = duels_list
        self.duels_number = duels_number
        self.duels_average = duels_average
        self.duels_stdev = duels_stdev
        self.combats_list = combats_list
        self.combats_numbers = combats_numbers
        self.combats_average = combats_average
        self.combats_stdev = combats_stdev
        self.rounds_number = rounds_number
        self.rounds_average = rounds_average
        self.rounds_stdev = rounds_stdev
        self.players_list = players_list
        self.players_number = players_number
        self.players_average = players_average
        self.players_stdev = players_stdev
        self.teams_list = teams_list
        self.teams_number = teams_number
        self.teams_average = teams_average
        self.teams_stdev = teams_stdev
        self.characters_list = characters_list
        self.characters_number = characters_number
        self.characters_average = characters_average
        self.characters_stdev = characters_stdev
        self.players_characters_list = players_characters_list
        self.players_characters_number = players_characters_number
        self.players_characters_average = players_characters_average
        self.players_characters_stdev = players_characters_stdev
        self.winners_player_list = winners_player_list
        self.winners_player_number = winners_player_number
        self.winners_team_list = winners_team_list
        self.winners_team_number = winners_team_number

    

class EventStats:
    ...

class DuelStats:
    ...

class CombatStats:
    ...

class RoundStats: # ???
    ...

class EntityStats:
    ...

class CompetitorStats:
    ...

class RoundResult:
    def __init__(self, winner, loser):
        self._winner = winner
        self._loser = loser

    ''' Methods '''
    @property
    def winner(self):
        return self._winner
    
    @property
    def loser(self):
        return self._loser


class RoundPlayerStats:
    def __init__(self, won, lost, beating_factor, points_raw):
        self._won = won
        self._lost = lost
        self._beating_factor = beating_factor
        self._points_raw = points_raw

    ''' Methods '''
    @property
    def won(self):
        return self._won
    
    @property
    def lost(self):
        return self._lost
    
    @property
    def beating_factor(self):
        return self._beating_factor
    
    @property
    def points_raw(self):
        return self._points_raw


''' FUNCTIONS '''

def win_rate(victories, played):
    return victories / played
    

def win_lose_ratio(func, victories, defeats):
    win_lose_ratio = 0
    if defeats == 0:
        win_lose_ratio = victories
    elif victories == 0:
        win_lose_ratio = 0.5 / defeats
    elif defeats == 1:
        win_lose_ratio = victories * (3 / 4)
    else:
        win_lose_ratio = victories / defeats
    return func(win_lose_ratio)


def beating_factor(victories, played):
    beating_factor = 0
    if victories == 0:
        beating_factor = (1 / played) / 2
    else:
        beating_factor = victories / played
    return beating_factor


def level_factor(a, b, win_rates_diff):
    return a * win_rates_diff + b


# def is_numeric_list(data_list):
#     return all(isinstance(element, numbers.Number) for element in data_list)
        

def get_statistics(data_list):
    '''
    data_list: numeric list
    '''
    mean = st.mean(data_list)
    median = st.median(data_list)
    mode = st.mode(data_list)
    stdev = st.stdev(data_list)
    variance = st.variance(data_list)
    return Statistics(mean, median, mode, stdev, variance)


def get_multimode(data_list):
    '''
    data_list: non numeric list
    '''
    return st.multimode(data_list)