import statistics as st
import numbers


''' UTILITY CLASES '''

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
                 events_tournament_list,
                 events_tournament_number,
                 events_tournament_rate,
                 events_league_list,
                 events_league_number,
                 events_league_rate,
                 duels_list,
                 duels_number,
                 duels_statistics,
                 combats_list,
                 combats_number,
                 combats_statistics,
                 rounds_list,
                 rounds_number,
                 rounds_statistics,
                 players_list,
                 players_number,
                 players_statistics,
                 players_most_participations,
                 teams_list,
                 teams_number,
                 teams_statistics,
                 teams_most_participations,
                 characters_list,
                 characters_number,
                 characters_statistics,
                 characters_most_participations,
                 player_characters_list,
                 player_characters_number,
                 player_characters_statistics,
                 player_characters_most_participations,
                 winners_player_list,
                 winners_player_number,
                 winners_team_list,
                 winners_team_number):
        self._events_list = events_list,
        self._events_number = events_number,
        self._events_player_list = events_player_list,
        self._events_player_number = events_player_number,
        self._events_player_rate = events_player_rate,
        self._events_team_list = events_team_list,
        self._events_team_number = events_team_number,
        self._events_team_rate = events_team_rate,
        self._events_tournament_list = events_tournament_list,
        self._events_tournament_number = events_tournament_number,
        self._events_tournament_rate = events_tournament_rate,
        self._events_league_list = events_league_list,
        self._events_league_number = events_league_number,
        self._events_league_rate = events_league_rate,
        self._duels_list = duels_list,
        self._duels_number = duels_number,
        self._duels_statistics = duels_statistics,
        self._combats_list = combats_list,
        self._combats_number = combats_number,
        self._combats_statistics = combats_statistics,
        self._rounds_list = rounds_list,
        self._rounds_number = rounds_number,
        self._rounds_statistics = rounds_statistics,
        self._players_list = players_list,
        self._players_number = players_number,
        self._players_statistics = players_statistics,
        self._players_most_participations = players_most_participations,
        self._teams_list = teams_list,
        self._teams_number = teams_number,
        self._teams_statistics = teams_statistics,
        self._teams_most_participations = teams_most_participations,
        self._characters_list = characters_list,
        self._characters_number = characters_number,
        self._characters_statistics = characters_statistics,
        self._characters_most_participations = characters_most_participations,
        self._player_characters_list = player_characters_list,
        self._player_characters_number = player_characters_number,
        self._player_characters_statistics = player_characters_statistics,
        self._player_characters_most_participations = player_characters_most_participations,
        self._winners_player_list = winners_player_list,
        self._winners_player_number = winners_player_number,
        self._winners_team_list = winners_team_list,
        self._winners_team_number = winners_team_number

    @property
    def events_list(self):
        return self._events_list

    @property
    def events_number(self):
        return self._events_number

    @property
    def events_player_list(self):
        return self._events_player_list

    @property
    def events_player_number(self):
        return self._events_player_number

    @property
    def events_player_rate(self):
        return self._events_player_rate

    @property
    def events_team_list(self):
        return self._events_team_list

    @property
    def events_team_number(self):
        return self._events_team_number

    @property
    def events_team_rate(self):
        return self._events_team_rate

    @property
    def events_tournament_list(self):
        return self._events_tournament_list

    @property
    def events_tournament_number(self):
        return self._events_tournament_number

    @property
    def events_tournament_rate(self):
        return self._events_tournament_rate

    @property
    def events_league_list(self):
        return self._events_league_list

    @property
    def events_league_number(self):
        return self._events_league_number

    @property
    def events_league_rate(self):
        return self._events_league_rate

    @property
    def duels_list(self):
        return self._duels_list

    @property
    def duels_number(self):
        return self._duels_number

    @property
    def duels_statistics(self):
        return self._duels_statistics

    @property
    def combats_list(self):
        return self._combats_list

    @property
    def combats_number(self):
        return self._combats_number

    @property
    def combats_statistics(self):
        return self._combats_statistics

    @property
    def rounds_list(self):
        return self._rounds_list

    @property
    def rounds_number(self):
        return self._rounds_number

    @property
    def rounds_statistics(self):
        return self._rounds_statistics

    @property
    def players_list(self):
        return self._players_list

    @property
    def players_number(self):
        return self._players_number

    @property
    def players_statistics(self):
        return self._players_statistics

    @property
    def players_most_participations(self):
        return self._players_most_participations

    @property
    def teams_list(self):
        return self._teams_list

    @property
    def teams_number(self):
        return self._teams_number

    @property
    def teams_statistics(self):
        return self._teams_statistics

    @property
    def teams_most_participations(self):
        return self._teams_most_participations

    @property
    def characters_list(self):
        return self._characters_list

    @property
    def characters_number(self):
        return self._characters_number

    @property
    def characters_statistics(self):
        return self._characters_statistics

    @property
    def characters_most_participations(self):
        return self._characters_most_participations

    @property
    def player_characters_list(self):
        return self._player_characters_list

    @property
    def player_characters_number(self):
        return self._player_characters_number

    @property
    def player_characters_statistics(self):
        return self._player_characters_statistics

    @property
    def player_characters_most_participations(self):
        return self._player_characters_most_participations

    @property
    def winners_player_list(self):
        return self._winners_player_list

    @property
    def winners_player_number(self):
        return self._winners_player_number

    @property
    def winners_team_list(self):
        return self._winners_team_list

    @property
    def winners_team_number(self):
        return self._winners_team_number

    
class EventStats:
    def __init__(self,
                 duels_list,
                 duels_number,
                 combats_list,
                 combats_number,
                 combats_statistics,
                 rounds_list,
                 rounds_number,
                 rounds_statistics,
                 competitors_list,
                 competitors_number,
                 competitors_statistics,
                 competitors_most_participations,
                 characters_list,
                 characters_number,
                 characters_statistics,
                 characters_most_participations,
                 player_characters_list,
                 player_characters_number,
                 player_characters_statistics,
                 player_characters_most_participations,
                 winner,
                 results):
        self._duels_list = duels_list,
        self._duels_number = duels_number,
        self._combats_list = combats_list,
        self._combats_number = combats_number,
        self._combats_statistics = combats_statistics,
        self._rounds_list = rounds_list,
        self._rounds_number = rounds_number,
        self._rounds_statistics = rounds_statistics,
        self._competitors_list = competitors_list,
        self._competitors_number = competitors_number,
        self._competitors_statistics = competitors_statistics,
        self._competitors_most_participations = competitors_most_participations,
        self._characters_list = characters_list,
        self._characters_number = characters_number,
        self._characters_statistics = characters_statistics,
        self._characters_most_participations = characters_most_participations,
        self._player_characters_list = player_characters_list,
        self._player_characters_number = player_characters_number,
        self._player_characters_statistics = player_characters_statistics,
        self._player_characters_most_participations = player_characters_most_participations,
        self._winner = winner,
        self._results = results

    @property
    def duels_list(self):
        return self._duels_list

    @property
    def duels_number(self):
        return self._duels_number

    @property
    def combats_list(self):
        return self._combats_list

    @property
    def combats_number(self):
        return self._combats_number

    @property
    def combats_statistics(self):
        return self._combats_statistics

    @property
    def rounds_list(self):
        return self._rounds_list

    @property
    def rounds_number(self):
        return self._rounds_number

    @property
    def rounds_statistics(self):
        return self._rounds_statistics

    @property
    def competitors_list(self):
        return self._competitors_list

    @property
    def competitors_number(self):
        return self._competitors_number

    @property
    def competitors_statistics(self):
        return self._competitors_statistics

    @property
    def competitors_most_participations(self):
        return self._competitors_most_participations

    @property
    def characters_list(self):
        return self._characters_list

    @property
    def characters_number(self):
        return self._characters_number

    @property
    def characters_statistics(self):
        return self._characters_statistics

    @property
    def characters_most_participations(self):
        return self._characters_most_participations

    @property
    def player_characters_list(self):
        return self._player_characters_list

    @property
    def player_characters_number(self):
        return self._player_characters_number

    @property
    def player_characters_statistics(self):
        return self._player_characters_statistics

    @property
    def player_characters_most_participations(self):
        return self._player_characters_most_participations

    @property
    def winner(self):
        return self._winner

    @property
    def results(self):
        return self._results


class DuelStats:
    def __init__(self,
                 combats_list,
                 combats_number,
                 rounds_list,
                 rounds_number,
                 rounds_statistics,
                 competitors_list,
                 competitors_number,
                 competitors_statistics,
                 competitors_most_participations,
                 characters_list,
                 characters_number,
                 characters_statistics,
                 characters_most_participations,
                 player_characters_list,
                 player_characters_number,
                 player_characters_statistics,
                 player_characters_most_participations,
                 results,
                 winner):
        self._combats_list = combats_list
        self._combats_number = combats_number
        self._rounds_list = rounds_list
        self._rounds_number = rounds_number
        self._rounds_statistics = rounds_statistics
        self._competitors_list = competitors_list
        self._competitors_number = competitors_number
        self._competitors_statistics = competitors_statistics
        self._competitors_most_participations = competitors_most_participations
        self._characters_list = characters_list
        self._characters_number = characters_number
        self._characters_statistics = characters_statistics
        self._characters_most_participations = characters_most_participations
        self._player_characters_list = player_characters_list
        self._player_characters_number = player_characters_number
        self._player_characters_statistics = player_characters_statistics
        self._player_characters_most_participations = player_characters_most_participations
        self._results = results
        self._winner = winner

    @property
    def combats_list(self):
        return self._combats_list

    @property
    def combats_number(self):
        return self._combats_number

    @property
    def rounds_list(self):
        return self._rounds_list

    @property
    def rounds_number(self):
        return self._rounds_number

    @property
    def rounds_statistics(self):
        return self._rounds_statistics

    @property
    def competitors_list(self):
        return self._competitors_list

    @property
    def competitors_number(self):
        return self._competitors_number

    @property
    def competitors_statistics(self):
        return self._competitors_statistics

    @property
    def competitors_most_participations(self):
        return self._competitors_most_participations

    @property
    def characters_list(self):
        return self._characters_list

    @property
    def characters_number(self):
        return self._characters_number

    @property
    def characters_statistics(self):
        return self._characters_statistics

    @property
    def characters_most_participations(self):
        return self._characters_most_participations

    @property
    def player_characters_list(self):
        return self._player_characters_list

    @property
    def player_characters_number(self):
        return self._player_characters_number

    @property
    def player_characters_statistics(self):
        return self._player_characters_statistics

    @property
    def player_characters_most_participations(self):
        return self._player_characters_most_participations

    @property
    def results(self):
        return self._results

    @property
    def winner(self):
        return self._winner


class CombatStats: # @@@@ pendiente
    def __init__(self,
                 rounds_list,
                 rounds_number,
                 competitors_list,
                 characters_list,
                 player_characters_list,
                 winner):
        self._rounds_list = rounds_list
        self._rounds_number = rounds_number
        self._competitors_list = competitors_list
        self._characters_list = characters_list
        self._player_characters_list = player_characters_list
        self._winner = winner

    @property
    def rounds_list(self):
        return self._rounds_list

    @property
    def rounds_number(self):
        return self._rounds_number

    @property
    def competitors_list(self):
        return self._competitors_list

    @property
    def characters_list(self):
        return self._characters_list

    @property
    def player_characters_list(self):
        return self._player_characters_list

    @property
    def winner(self):
        return self._winner


class CombatData:
    def __init__(self,
                 win_points_competitor1,
                 win_points_competitor2,
                 points_earned_competitor1,
                 points_earned_competitor2):
        self._win_points_competitor1 = win_points_competitor1
        self._win_points_competitor2 = win_points_competitor2
        self._points_earned_competitor1 = points_earned_competitor1
        self._points_earned_competitor2 = points_earned_competitor2
    
    @property
    def win_points_competitor1(self):
        return self._win_points_competitor1

    @property
    def win_points_competitor2(self):
        return self._win_points_competitor2

    @property
    def points_earned_competitor1(self):
        return self._points_earned_competitor1

    @property
    def points_earned_competitor2(self):
        return self._points_earned_competitor2


class CombatsData:
    def __init__(self,
                 win_points,
                 points_earned):
        self._win_points = win_points
        self._points_earned = points_earned

    @property
    def win_points(self):
        return self._win_points

    @property
    def points_earned(self):
        return self._points_earned


class RoundData:
    def __init__(self,
                 points_player1,
                 points_player2,
                 result_player1,
                 result_player2):
        self._points_player1 = points_player1
        self._points_player2 = points_player2
        self._result_player1 = result_player1
        self._result_player2 = result_player2

    @property    
    def points_player1(self):
        return self._points_player1

    @property        
    def points_player2(self):
        return self._points_player2

    @property        
    def result_player1(self):
        return self._result_player1

    @property        
    def result_player2(self):
        return self._result_player2


class EntityStats:
    ...

class CompetitorStats:
    ...

class CombatResult:
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


class CombatPlayerStats:
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


class CombatsStats:
    def __init__(self,
                 combats_won_list,
                 combats_lost_list,
                 combats_draw_list,
                 combats_won_number,
                 combats_lost_number,
                 combats_draw_number,
                 combats_win_rate,
                 rounds_played_number,
                 rounds_won_number,
                 rounds_lost_number,
                 rounds_win_rate):
        self._combats_won_list = combats_won_list
        self._combats_lost_list = combats_lost_list
        self._combats_draw_list = combats_draw_list
        self._combats_won_number = combats_won_number
        self._combats_lost_number = combats_lost_number
        self._combats_draw_number = combats_draw_number
        self._combats_win_rate = combats_win_rate
        self._rounds_played_number = rounds_played_number
        self._rounds_won_number = rounds_won_number
        self._rounds_lost_number = rounds_lost_number
        self._rounds_win_rate = rounds_win_rate
        
    ''' Methods '''
    @property
    def combats_won_list(self):
        return self._combats_won_list

    @property
    def combats_lost_list(self):
        return self._combats_lost_list

    @property
    def combats_draw_list(self):
        return self._combats_draw_list

    @property
    def combats_won_number(self):
        return self._combats_won_number

    @property
    def combats_lost_number(self):
        return self._combats_lost_number

    @property
    def combats_draw_number(self):
        return self._combats_draw_number

    @property
    def combats_win_rate(self):
        return self._combats_win_rate

    @property
    def rounds_played_number(self):
        return self._rounds_played_number

    @property
    def rounds_won_number(self):
        return self._rounds_won_number

    @property
    def rounds_lost_number(self):
        return self._rounds_lost_number

    @property
    def rounds_win_rate(self):
        return self._rounds_win_rate


class DuelsStats:
    def __init__(self,
                 played_list,
                 won_list,
                 lost_list,
                 played_number,
                 won_number,
                 lost_number,
                 win_rate):
        self._played_list = played_list
        self._won_list = won_list
        self._lost_list = lost_list
        self._played_number = played_number
        self._won_number = won_number
        self._lost_number = lost_number
        self._win_rate = win_rate
    
    ''' Methods '''
    @property
    def played_list(self):
        return self._played_list

    @property
    def won_list(self):
        return self._won_list

    @property
    def lost_list(self):
        return self._lost_list

    @property
    def played_number(self):
        return self._played_number

    @property
    def won_number(self):
        return self._won_number

    @property
    def lost_number(self):
        return self._lost_number

    @property
    def win_rate(self):
        return self._win_rate




''' RANKING FUNCTIONS '''

def win_rate(victories, played):
    ''' Challenges won over challanges played. '''
    return victories / played
    

def win_lose_ratio(func, victories, defeats):
    ''' Balancing factor. Victories over defeats with some considerations. '''
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
    ''' Like win rate but with a consideration when victories are zero. '''
    beating_factor = 0
    if victories == 0:
        beating_factor = (1 / played) / 2
    else:
        beating_factor = victories / played
    return beating_factor


def level_factor(a, b, win_rates_diff):
    ''' Level factor to equate competitors with different skill level. '''
    return a * win_rates_diff + b

        
''' STATISTICS FUNCTIONS '''

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