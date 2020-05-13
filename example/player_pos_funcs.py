parser = None
demo_path = r"C:\Users\Zahar\Desktop\asd\demo.dem"
dump_file = open(r"C:\Users\Zahar\Desktop\asd\demo_dump.txt", "w", encoding="utf-8")
# in_game_round_time = 0
PLAYERS = list()


class MyPlayer:
    def __init__(self, entity, userinfo):
        self.entity = entity
        self.userinfo = userinfo


def begin_new_match(data):
    # this event happens after warmup ends
    dump_file.write("MATCH STARTED\nROUND 1 .....................................................................\n")


def round_officially_ended(data):
    # this event happens every time a round ends
    current_round = get_one_entity("CCSGameRulesProxy").get_prop("m_totalRoundsPlayed")
    dump_file.write("ROUND {} ..........................................................\n".format(current_round))


def round_freeze_end(data):
    # get player entities again since some may disconnect / reconnect in freeze time
    bind_player_entities()


def print_player_positions(data):
    global PLAYERS
    if not len(PLAYERS):
        return
    for player in PLAYERS:
        pos = player.entity.get_table("DT_CSLocalPlayerExclusive")
        dump_file.write("{} is at x: {} / ".format(player.userinfo.name, pos["m_vecOrigin"]["x"]))
        dump_file.write("y: {} / z: {}\n".format(pos["m_vecOrigin"]["y"], pos["m_vecOrigin[2]"]))
    dump_file.write("\n")


def bind_player_entities():
    global PLAYERS
    PLAYERS.clear()
    # looking for players through the "userinfo" table
    for table in parser._string_tables_list:
        if table.name == "userinfo":
            for player in table.data:
                # ud is a UserInfo instance from structures.py
                # entry is the entity id - 1
                ud = player["user_data"]
                entry = player["entry"]
                if not ud or not entry or ud.guid == "BOT":
                    continue
                player2 = parser._entities.get(int(player["entry"]) + 1)
                if player2:
                    PLAYERS.append(MyPlayer(player2, ud))
            break


def get_one_entity(text):
    for ent in parser._entities.values():
        if ent and ent.class_name == text:
            return ent
