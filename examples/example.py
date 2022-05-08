from splatnet.splatnet2 import Config, Splatnet2

config = Config()
splatnet = Splatnet2(config)

results = splatnet.results()

total_paint_point = 0
team_total_kill_count = 0

for r in results.results:
    total_paint_point += r.player_result.game_paint_point

    # Get all data of a battle
    result = splatnet.result(r.battle_number)

    for player_result in result.my_team_members:
        team_total_kill_count += player_result.kill_count

    team_total_kill_count += result.player_result.kill_count

print(f"{total_paint_point=}")
print(f"{team_total_kill_count=}")
