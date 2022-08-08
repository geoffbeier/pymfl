from pymfl.api.MFLAPIClient import MFLAPIClient


class FantasyContentAPIClient(MFLAPIClient):

    @classmethod
    def get_players(cls, *, year: int, league_id: str, **kwargs) -> dict:
        """
        TODO: caching for this method
        All player IDs, names and positions that MyFantasyLeague.com has in our database for the current year.
        All other data types refer only to player IDs, so if you'd like to later present any data to people,
        you'll need this data type for translating player IDs to player names.
        Our player database is updated at most once per day, and it contains more than 2,000 players.
        In other words, you're strongly encouraged to read this data type no more than once per day and store it locally as needed to optimize your system performance.
        """
        filters = [("TYPE", "players"), ("JSON", 1)]
        # Set this value to 1 to return complete player details, including player IDs from other sources.
        details: int = kwargs.pop("details", None)
        # Pass a unix timestamp via this parameter to receive only changes to the player database since that time.
        since: str = kwargs.pop("since", None)
        # Pass a list of player ids separated by commas (or just a single player id) to receive back just the info on those players.
        players = kwargs.pop("players", None)
        cls._add_filter_if_given("DETAILS", details, filters)
        cls._add_filter_if_given("SINCE", since, filters)
        cls._add_filter_if_given("PLAYERS", players, filters)
        url = cls._build_route(cls._MFL_APP_BASE_URL, year, cls._EXPORT_ROUTE)
        url = cls._add_filters(url, *filters)
        return cls._get_for_year_and_league_id(url=url, year=year, league_id=league_id)

    @classmethod
    def get_player_profile(cls, *, year: int, league_id: str, player_id_or_ids: str) -> dict:
        """
        Returns a summary of information regarding a player, including DOB, ADP ranking, height/weight.

        player_id_or_ids: Player id or list of player ids separated by commas
        """
        filters = [("TYPE", "playerProfile"), ("P", player_id_or_ids), ("JSON", 1)]
        url = cls._build_route(cls._MFL_APP_BASE_URL, year, cls._EXPORT_ROUTE)
        url = cls._add_filters(url, *filters)
        return cls._get_for_year_and_league_id(url=url, year=year, league_id=league_id)

    @classmethod
    def get_all_rules(cls, *, year: int, league_id: str) -> dict:
        """
        All scoring rules that MyFantasyLeague.com currently supports, including:
        if the rule is scored for players, teams or coaches, as well as an abbreviation of the scoring rule, a short description, and a detailed description.
        If you plan on using the 'rules' data type, you'll also need this data type to look up the abbreviations to translate them to their detailed description for people.
        """
        filters = [("TYPE", "allRules"), ("JSON", 1)]
        url = cls._build_route(cls._MFL_APP_BASE_URL, year, cls._EXPORT_ROUTE)
        url = cls._add_filters(url, *filters)
        return cls._get_for_year_and_league_id(url=url, year=year, league_id=league_id)

    @classmethod
    def get_player_ranks(cls, *, year: int, league_id: str, **kwargs) -> dict:
        """
        This report provides overall player rankings from the experts at FantasySharks.com.
        These rankings can be used instead of Average Draft Position (ADP) rankings for guidance during your draft, or when generating your own draft list.
        """
        filters = [("TYPE", "playerRanks"), ("JSON", 1)]
        position = kwargs.pop("POS", None)
        cls._add_filter_if_given("POS", position, filters)
        url = cls._build_route(cls._MFL_APP_BASE_URL, year, cls._EXPORT_ROUTE)
        url = cls._add_filters(url, *filters)
        return cls._get_for_year_and_league_id(url=url, year=year, league_id=league_id)
