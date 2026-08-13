import json


def transform_cricket_data(api_response):
    """
    Convert CricAPI response into a flat list of match records.
    One dictionary = one match.

    If the API provides fewer than two teams, the function attempts
    to extract the teams from the match name.
    """

    matches = api_response.get("data", [])

    transformed_data = []

    for match in matches:

        match_name = match.get("name")
        teams = match.get("teams") or []

        # --------------------------------------------------------
        # Get teams from API
        # --------------------------------------------------------

        team1 = teams[0] if len(teams) > 0 else None
        team2 = teams[1] if len(teams) > 1 else None

        # --------------------------------------------------------
        # Fallback: extract teams from match name
        # Example:
        # Hong Kong, China Women vs Tanzania Women, 3rd Match, ...
        #
        # Becomes:
        # team1 = Hong Kong, China Women
        # team2 = Tanzania Women
        # --------------------------------------------------------

        if (team1 is None or team2 is None) and match_name:
            if " vs " in match_name:

                match_parts = match_name.split(" vs ", 1)

                extracted_team1 = match_parts[0].strip()
                extracted_team2 = match_parts[1].split(",", 1)[0].strip()

                if extracted_team1:
                    team1 = extracted_team1

                if extracted_team2:
                    team2 = extracted_team2

        transformed_data.append({
            "match_id": match.get("id"),
            "match_name": match_name,
            "match_type": match.get("matchType"),
            "status": match.get("status"),
            "venue": match.get("venue"),
            "match_date": match.get("date"),
            "match_datetime_gmt": match.get("dateTimeGMT"),

            "team1": team1,
            "team2": team2,

            "series_id": match.get("series_id"),

            "fantasy_enabled": match.get("fantasyEnabled"),
            "bbb_enabled": match.get("bbbEnabled"),
            "has_squad": match.get("hasSquad"),
            "match_started": match.get("matchStarted"),
            "match_ended": match.get("matchEnded")
        })

    print(f"✅ Transformed {len(transformed_data)} matches.")

    return transformed_data


if __name__ == "__main__":

    with open("sample.json", "r") as f:
        api_data = json.load(f)

    transformed = transform_cricket_data(api_data)

    print(json.dumps(transformed[:2], indent=4))