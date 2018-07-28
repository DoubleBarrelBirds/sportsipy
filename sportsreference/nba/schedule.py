import re
from .constants import (SCHEDULE_SCHEME,
                        SCHEDULE_URL)
from datetime import datetime
from pyquery import PyQuery as pq
from sportsreference import utils
from sportsreference.constants import (WIN,
                                       LOSS,
                                       HOME,
                                       AWAY,
                                       NEUTRAL,
                                       REGULAR_SEASON,
                                       CONFERENCE_TOURNAMENT)
from sportsreference.nba.boxscore import Boxscore


class Game(object):
    """
    A representation of a matchup between two teams.

    Stores all relevant high-level match information for a game in a team's
    schedule including date, time, opponent, and result.
    """
    def __init__(self, game_data):
        """
        Parse all of the attributes located in the HTML data.

        Parameters
        ----------
        game_data : string
            The row containing the specified game information.
        """
        self._game = None
        self._date = None
        self._datetime = None
        self._boxscore = None
        self._location = None
        self._opponent_abbr = None
        self._result = None
        self._points_scored = None
        self._points_allowed = None
        self._field_goals = None
        self._field_goal_attempts = None
        self._field_goal_percentage = None
        self._three_point_field_goals = None
        self._three_point_field_goal_attempts = None
        self._three_point_field_goal_percentage = None
        self._free_throws = None
        self._free_throw_attempts = None
        self._free_throw_percentage = None
        self._offensive_rebounds = None
        self._total_rebounds = None
        self._assists = None
        self._steals = None
        self._blocks = None
        self._turnovers = None
        self._personal_fouls = None
        self._opp_field_goals = None
        self._opp_field_goal_attempts = None
        self._opp_field_goal_percentage = None
        self._opp_three_point_field_goals = None
        self._opp_three_point_field_goal_attempts = None
        self._opp_three_point_field_goal_percentage = None
        self._opp_free_throws = None
        self._opp_free_throw_attempts = None
        self._opp_free_throw_percentage = None
        self._opp_offensive_rebounds = None
        self._opp_total_rebounds = None
        self._opp_assists = None
        self._opp_steals = None
        self._opp_blocks = None
        self._opp_turnovers = None
        self._opp_personal_fouls = None

        self._parse_game_data(game_data)

    def _parse_boxscore(self, game_data):
        """
        Parses the boxscore URI for the game.

        The boxscore is embedded within the HTML tag and needs a special
        parsing scheme in order to be extracted.
        """
        boxscore = game_data('td[data-stat="box_score_text"]:first')
        boxscore = re.sub(r'.*/boxscores/', '', str(boxscore))
        boxscore = re.sub('\.html.*', '', boxscore)
        setattr(self, '_boxscore', boxscore)

    def _parse_game_data(self, game_data):
        """
        Parses a value for every attribute.

        The function looks through every attribute with the exception of those
        listed below and retrieves the value according to the parsing scheme
        and index of the attribute from the passed HTML data. Once the value
        is retrieved, the attribute's value is updated with the returned
        result.

        Note that this method is called directory once Game is invoked and does
        not need to be called manually.

        Parameters
        ----------
        game_data : string
            A string containing all of the rows of stats for a given game.
        """
        for field in self.__dict__:
            # Remove the leading '_' from the name
            short_name = str(field)[1:]
            if short_name == 'datetime':
                continue
            elif short_name == 'boxscore':
                self._parse_boxscore(game_data)
                continue
            value = utils._parse_field(SCHEDULE_SCHEME, game_data, short_name)
            setattr(self, field, value)

    @property
    def game(self):
        """
        Returns an int to indicate which game in the season was requested. The
        first game of the season returns 1.
        """
        return int(self._game)

    @property
    def date(self):
        """
        Returns a string of the date the game took place at, such as 'Wed, Oct
        18, 2017'.
        """
        return self._date

    @property
    def datetime(self):
        """
        Returns a datetime object to indicate the month, day, and year the game
        took place.
        """
        return datetime.strptime(self._date, '%Y-%m-%d')

    @property
    def boxscore(self):
        """
        Returns an instance of the Boxscore class containing more detailed
        stats on the game.
        """
        return Boxscore(self._boxscore)

    @property
    def location(self):
        """
        Returns a string constant to indicate whether the game was played in
        the team's home arena or on the road.
        """
        if self._location.lower() == '@':
            return AWAY
        return HOME

    @property
    def opponent_abbr(self):
        """
        Returns a string of the opponent's 3-letter abbreviation, such as 'CHI'
        for the Chicago Bulls.
        """
        return self._opponent_abbr

    @property
    def result(self):
        """
        Returns a string constant to indicate whether the team won or lost the
        game.
        """
        if self._result.lower() == 'l':
            return LOSS
        return WIN

    @property
    def points_scored(self):
        """
        Returns an int of the number of points the team scored during the game.
        """
        return int(self._points_scored)

    @property
    def points_allowed(self):
        """
        Returns an int of the number of points the team allowed during the
        game.
        """
        return int(self._points_allowed)

    @property
    def field_goals(self):
        """
        Returns an int of the total number of field goals made by the team.
        """
        return int(self._field_goals)

    @property
    def field_goal_attempts(self):
        """
        Returns an int of the total number of field goal attempts by the team.
        """
        return int(self._field_goal_attempts)

    @property
    def field_goal_percentage(self):
        """
        Returns a float of the number of field goals made divided by the total
        number of field goal attempts by the team. Percentage ranges from
        0-1.
        """
        return float(self._field_goal_percentage)

    @property
    def three_point_field_goals(self):
        """
        Returns an int of the total number of three point field goals made
        by the team.
        """
        return int(self._three_point_field_goals)

    @property
    def three_point_field_goal_attempts(self):
        """
        Returns an int of the total number of three point field goal attempts
        by the team.
        """
        return int(self._three_point_field_goal_attempts)

    @property
    def three_point_field_goal_percentage(self):
        """
        Returns a float of the number of three point field goals made divided
        by the number of three point field goal attempts by the team.
        Percentage ranges from 0-1.
        """
        return float(self._three_point_field_goal_percentage)

    @property
    def free_throws(self):
        """
        Returns an int of the total number of free throws made by the team.
        """
        return int(self._free_throws)

    @property
    def free_throw_attempts(self):
        """
        Returns an int of the total number of free throw attempts by the team.
        """
        return int(self._free_throw_attempts)

    @property
    def free_throw_percentage(self):
        """
        Returns a float of the number of free throws made divided by the number
        of free throw attempts by the team.
        """
        return float(self._free_throw_percentage)

    @property
    def offensive_rebounds(self):
        """
        Returns an int of the total number of offensive rebounds by the team.
        """
        return int(self._offensive_rebounds)

    @property
    def total_rebounds(self):
        """
        Returns an int of the total number of rebounds by the team.
        """
        return int(self._total_rebounds)

    @property
    def assists(self):
        """
        Returns an int of the total number of assists by the team.
        """
        return int(self._assists)

    @property
    def steals(self):
        """
        Returns an int of the total number of steals by the team.
        """
        return int(self._steals)

    @property
    def blocks(self):
        """
        Returns an int of the total number of blocks by the team.
        """
        return int(self._blocks)

    @property
    def turnovers(self):
        """
        Returns an int of the total number of turnovers by the team.
        """
        return int(self._turnovers)

    @property
    def personal_fouls(self):
        """
        Returns an int of the total number of personal fouls by the team.
        """
        return int(self._personal_fouls)

    @property
    def opp_field_goals(self):
        """
        Returns an int of the total number of field goals made by the opponent.
        """
        return int(self._opp_field_goals)

    @property
    def opp_field_goal_attempts(self):
        """
        Returns an int of the total number of field goal attempts by the
        opponent.
        """
        return int(self._opp_field_goal_attempts)

    @property
    def opp_field_goal_percentage(self):
        """
        Returns a float of the number of field goals made divided by the total
        number of field goal attempts by the opponent. Percentage ranges from
        0-1.
        """
        return float(self._opp_field_goal_percentage)

    @property
    def opp_three_point_field_goals(self):
        """
        Returns an int of the total number of three point field goals made
        by the opponent.
        """
        return int(self._opp_three_point_field_goals)

    @property
    def opp_three_point_field_goal_attempts(self):
        """
        Returns an int of the total number of three point field goal attempts
        by the opponent.
        """
        return int(self._opp_three_point_field_goal_attempts)

    @property
    def opp_three_point_field_goal_percentage(self):
        """
        Returns a float of the number of three point field goals made divided
        by the number of three point field goal attempts by the opponent.
        Percentage ranges from 0-1.
        """
        return float(self._opp_three_point_field_goal_percentage)

    @property
    def opp_free_throws(self):
        """
        Returns an int of the total number of free throws made by the opponent.
        """
        return int(self._opp_free_throws)

    @property
    def opp_free_throw_attempts(self):
        """
        Returns an int of the total number of free throw attempts by the
        opponent.
        """
        return int(self._opp_free_throw_attempts)

    @property
    def opp_free_throw_percentage(self):
        """
        Returns a float of the number of free throws made divided by the number
        of free throw attempts by the opponent.
        """
        return float(self._opp_free_throw_percentage)

    @property
    def opp_offensive_rebounds(self):
        """
        Returns an int of the total number of offensive rebounds by the
        opponent.
        """
        return int(self._opp_offensive_rebounds)

    @property
    def opp_total_rebounds(self):
        """
        Returns an int of the total number of rebounds by the opponent.
        """
        return int(self._opp_total_rebounds)

    @property
    def opp_assists(self):
        """
        Returns an int of the total number of assists by the opponent.
        """
        return int(self._opp_assists)

    @property
    def opp_steals(self):
        """
        Returns an int of the total number of steals by the opponent.
        """
        return int(self._opp_steals)

    @property
    def opp_blocks(self):
        """
        Returns an int of the total number of blocks by the opponent.
        """
        return int(self._opp_blocks)

    @property
    def opp_turnovers(self):
        """
        Returns an int of the total number of turnovers by the opponent.
        """
        return int(self._opp_turnovers)

    @property
    def opp_personal_fouls(self):
        """
        Returns an int of the total number of personal fouls by the opponent.
        """
        return int(self._opp_personal_fouls)


class Schedule:
    """
    An object of the given team's schedule.

    Generates a team's schedule for the season including wins, losses, and
    scores if applicable.
    """
    def __init__(self, abbreviation, year=None):
        """
        Parameters
        ----------
        abbreviation : string
            A team's short name, such as 'PHO' for the Phoenix Suns.
        year : string (optional)
            The requested year to pull stats from.
        """
        self._games = []
        self._pull_schedule(abbreviation, year)

    def __getitem__(self, index):
        """
        Return a specified game.

        Returns a specified game as requested by the index number in the array.
        The input index is 0-based and must be within the range of the schedule
        array.

        Parameters
        ----------
        index : int
            The 0-based index of the game to return.

        Returns
        -------
        Game instance
            If the requested game can be found, its Game instance is returned.
        """
        return self._games[index]

    def __call__(self, date):
        """
        Return a specified game.

        Returns a specific game as requested by the passed datetime. The input
        datetime must have the same year, month, and day, but can have any time
        be used to match the game.

        Parameters
        ----------
        date : datetime
            A datetime object of the month, day, and year to identify a
            particular game that was played.

        Returns
        -------
        Game instance
            If the requested game can be found, its Game instance is returned.

        Raises
        ------
        ValueError
            If the requested date cannot be matched with a game in the
            schedule.
        """
        for game in self._games:
            if game.datetime.year == date.year and \
               game.datetime.month == date.month and \
               game.datetime.day == date.day:
                return game
        raise ValueError('No games found for requested date')

    def __repr__(self):
        """Returns a list of all games scheduled for the given team."""
        return self._games

    def __iter__(self):
        """
        Returns an iterator of all of the games scheduled for the given team.
        """
        return iter(self.__repr__())

    def __len__(self):
        """Returns the number of scheduled games for the given team."""
        return len(self.__repr__())

    def _add_games_to_schedule(self, schedule):
        """
        Add game information to list of games.

        Create a Game instance for the given game in the schedule and add it to
        the list of games the team has or will play during the season.

        Parameters
        ----------
        schedule : PyQuery object
            A PyQuery object pertaining to a team's schedule table.
        year : string
            The requested year to pull stats from.
        """
        for item in schedule:
            if 'class="thead"' in str(item) or \
               'class="over_header thead"' in str(item):
                continue
            game = Game(item)
            self._games.append(game)

    def _pull_schedule(self, abbreviation, year):
        """
        Parameters
        ----------
        abbreviation : string
            A team's short name, such as 'DET' for the Detroit Pistons.
        year : string
            The requested year to pull stats from.
        """
        if not year:
            year = utils._find_year_for_season('nba')
        doc = pq(SCHEDULE_URL % (abbreviation, year))
        schedule = utils._get_stats_table(doc, 'table#tgl_basic')
        self._add_games_to_schedule(schedule)
        if 'tgl_basic_playoffs' in str(doc):
            playoffs = utils._get_stats_table(doc,
                                              'div#all_tgl_basic_playoffs')
            self._add_games_to_schedule(playoffs)
