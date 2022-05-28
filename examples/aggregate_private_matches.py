from collections import defaultdict
from datetime import date

from splatnet.splatnet2 import Config, Splatnet2


def aggregate(performances, player_result, team_result):
    player = player_result.player.nickname

    if player not in performances:
        performances[player] = defaultdict(lambda: 0)

    performances[player]["assist_count"] += player_result.assist_count
    performances[player]["death_count"] += player_result.death_count
    performances[player]["game_paint_point"] += player_result.game_paint_point
    performances[player]["kill_count"] += player_result.kill_count
    performances[player]["special_count"] += player_result.special_count

    if team_result.key == "victory":
        performances[player]["victory"] += 1
    else:
        performances[player]["defeat"] += 1


config = Config()
splatnet = Splatnet2(config)

results = splatnet.results()

count = 0
latest_date = None
performances = {}


for r in results.results:
    # Get detailed result
    result = splatnet.result(r.battle_number)

    if result.game_mode.key != "private":
        continue

    # Store date of the latest match and ignore matches played on other days.
    if latest_date is None:
        latest_date = date.fromtimestamp(result.start_time)
    elif latest_date != date.fromtimestamp(result.start_time):
        continue

    count += 1

    aggregate(performances, result.player_result, result.my_team_result)

    for player_result in result.my_team_members:
        aggregate(performances, player_result, result.my_team_result)

    for player_result in result.other_team_members:
        aggregate(performances, player_result, result.other_team_result)


for name, performance in performances.items():
    print(name)
    print(f"Game paint point: {performance['game_paint_point']}")
    print(f"Kill count:       {performance['kill_count']}")
    print(f"Assist count:     {performance['assist_count']}")
    print(f"Special count:    {performance['special_count']}")
    print(f"Death count:      {performance['death_count']}")
    print(f"Victory count:    {performance['victory']}")
    print(f"Defeat count:     {performance['defeat']}")
    print("--------------------------------")
