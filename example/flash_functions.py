match_started = False
round_current = 1
max_players = 10
PLAYERS_BY_UID = dict()
tickrate = 0
current_tick = 0
file = None
sec_threshold = 0


def player_blind(data):
    v = PLAYERS_BY_UID.get(data["userid"])
    a = PLAYERS_BY_UID.get(data["attacker"])
    time = round(data["blind_duration"], 2)
    if not v or not a:
        return
    # print(ve.get_prop("m_flFlashMaxAlpha"))
    # print(ve.get_prop("m_flFlashDuration"))
    if time > sec_threshold and not v.dead and time > remaining_flash_time(v):
        v.flashedby = a
        v.lastflashdur = time
        v.lastflashtick = current_tick
        if v.start_team == a.start_team:
            file.write("TF > {} flashed {} for {}s\n".format(a.name, v.name, time))
            a.teamflashes += 1
            a.teamflashesduration += time
        else:
            file.write("EF > {} flashed {} for {}s\n".format(a.name, v.name, time))
            a.enemyflashes += 1
            a.enemyflashesduration += time


def player_death(data):
    if match_started:
        d = PLAYERS_BY_UID.get(data["userid"])
        if not d:
            return
        d.dead = True
        if not d.flashedby:
            return
        if d.start_team == d.flashedby.start_team:
            file.write("TD > {} died flashed by {}\n".format(d.name, d.flashedby.name))
            d.flashedby.ftotd += 1
        else:
            file.write("ED > {} died flashed by {}\n".format(d.name, d.flashedby.name))
            d.flashedby.ftoed += 1


def player_team(data):
    global PLAYERS_BY_UID, max_players, round_current
    # trying to find out player teams (and bots, mainly bots here) since i'm not parsing entities
    # if data["isbot"]:
    #     print("bot {} joined team {} / disc= {}".format(data["userid"], data["team"], data["disconnect"]))
    # else:
    #     print("player {} joined team {} / disc= {}".format(data["userid"], data["team"], data["disconnect"]))
    if data["team"] == 0 or data["isbot"]:
        return
    rp = PLAYERS_BY_UID.get(data["userid"])
    if rp and rp.start_team is None:
        if max_players == 10:
            if round_current <= 15:
                if data["team"] in (2, 3):
                    rp.start_team = data["team"]
            else:
                if data["team"] == 2:
                    rp.start_team = 3
                elif data["team"] == 3:
                    rp.start_team = 2
        elif max_players == 4:
            if round_current <= 8:
                if data["team"] in (2, 3):
                    rp.start_team = data["team"]
            else:
                if data["team"] == 2:
                    rp.start_team = 3
                elif data["team"] == 3:
                    rp.start_team = 2


def player_spawn(data):
    global PLAYERS_BY_UID, max_players, round_current
    # trying to find out player teams since i'm not parsing entities
    if data["teamnum"] == 0:
        return
    rp = PLAYERS_BY_UID.get(data["userid"])
    if rp and rp.start_team is None:
        if max_players == 10:
            if round_current <= 15:
                if data["teamnum"] in (2, 3):
                    rp.start_team = data["teamnum"]
            else:
                if data["teamnum"] == 2:
                    rp.start_team = 3
                elif data["teamnum"] == 3:
                    rp.start_team = 2
        elif max_players == 4:
            if round_current <= 8:
                if data["teamnum"] in (2, 3):
                    rp.start_team = data["teamnum"]
            else:
                if data["teamnum"] == 2:
                    rp.start_team = 3
                elif data["teamnum"] == 3:
                    rp.start_team = 2


def begin_new_match(data):
    global match_started, file
    if match_started:
        _reset_pstats()
    match_started = True
    file.write("\nMATCH STARTED.....................................................................\n")
    # print("MATCH STARTED.....................................................................")


def round_officially_ended(data):
    global match_started, round_current, file
    if match_started:
        # STATS.update({round_current: MyRoundStats(team_score[2], team_score[3], PLAYERS)})
        round_current += 1
    file.write("\nROUND {}..........................................................\n".format(round_current))
    for p in PLAYERS_BY_UID.values():
        if p:
            p.dead = False
    # print("ROUND {}..........................................................".format(round_current))


def match_ended(data):
    global file
    file.write("\nMATCH ENDED.....................................................................\n")


def _reset_pstats():
    global PLAYERS_BY_UID
    for p2 in PLAYERS_BY_UID.values():
        p2.start_team = None


def update_pinfo(data):
    global PLAYERS_BY_UID, max_players
    if data.guid != "BOT":
        exist = None
        for x in PLAYERS_BY_UID.items():
            if data.xuid == x[1].userinfo.xuid:
                exist = x[0]
                break
        if exist:
            PLAYERS_BY_UID[exist].update(data, ui=True)
            if exist != data.user_id:
                PLAYERS_BY_UID.update({data.user_id: PLAYERS_BY_UID[exist]})
                PLAYERS_BY_UID.pop(exist)
        else:
            PLAYERS_BY_UID.update({data.user_id: MyPlayer(data, ui=True)})
        max_players = len(PLAYERS_BY_UID)


def new_demo(data):
    global match_started, round_current, PLAYERS_BY_UID, tickrate, current_tick
    current_tick = 0
    tickrate = int(data.ticks / data.playback_time)
    match_started = False
    round_current = 1
    PLAYERS_BY_UID = dict()


def print_end_stats(data):
    global file
    data1 = sorted(PLAYERS_BY_UID.values(), key=lambda x: x.teamflashesduration, reverse=True)
    data2 = sorted(PLAYERS_BY_UID.values(), key=lambda x: x.enemyflashesduration, reverse=True)
    file.write("\nTEAM FLASH STATS:\n\n")
    for p in data1:
        file.write("{} blinded teammates {} ".format(fix_len_string(p.name, 20), fix_len_string(p.teamflashes, 2)))
        file.write("times for {}s ".format(fix_len_string(round(p.teamflashesduration, 2), 5)))
        file.write("resulting in {} team deaths\n".format(fix_len_string(p.ftotd, 2)))
    file.write("\nENEMY FLASH STATS:\n\n")
    for p in data2:
        file.write("{} blinded enemies {} ".format(fix_len_string(p.name, 20), fix_len_string(p.enemyflashes, 2)))
        file.write("times for {}s ".format(fix_len_string(round(p.enemyflashesduration, 2), 5)))
        file.write("resulting in {} enemy deaths\n".format(fix_len_string(p.ftoed, 2)))


def get_entities(data):
    global current_tick
    # PLAYER_ENTITIES.clear()
    current_tick = data[1]
    for p in PLAYERS_BY_UID.values():
        # PLAYER_ENTITIES.update({p.userinfo.entity_id: data[0].get(p.userinfo.entity_id)})
        # if PLAYER_ENTITIES.get(p.userinfo.entity_id) and PLAYER_ENTITIES[p.userinfo.entity_id].get_prop("m_flFlashMaxAlpha"):
        #     print("alpha", PLAYER_ENTITIES[p.userinfo.entity_id].get_prop("m_flFlashMaxAlpha"))
        #     print(PLAYER_ENTITIES[p.userinfo.entity_id].get_prop("m_flFlashDuration"))
        if p.flashedby and not remaining_flash_time(p):
            # file.write("FLASH EXPIRED FOR {} AT {}\n".format(p.name, current_tick))
            p.flashedby = None


def remaining_flash_time(player):
    timesinceflash = (current_tick - player.lastflashtick) / tickrate
    # print(player.name, timesinceflash, player.lastflashdur)
    if timesinceflash >= player.lastflashdur:
        # print(player.name, timesinceflash, player.lastflashdur)
        return 0
    return timesinceflash


def fix_len_string(text, le):
    text = str(text)
    if len(text) > le:
        return text[:le]
    else:
        while len(text) != le:
            text += " "
        return text


class MyPlayer:
    def __init__(self, data=None, ui=False):
        self.teamflashes = 0
        self.enemyflashes = 0
        self.teamflashesduration = 0
        self.enemyflashesduration = 0
        self.ftotd = 0
        self.ftoed = 0
        self.flashedby = None
        self.lastflashdur = 0
        self.lastflashtick = 0
        self.dead = True
        self.id = None
        self.name = None
        self.profile = None
        # 2 = "T" // 3 = "CT"
        self.start_team = None
        self.userinfo = None
        if data:
            self.update(data, ui)

    def update(self, data, ui=False):
        if ui:
            self.userinfo = data
            self.id = data.user_id
            self.name = data.name
            self.profile = "https://steamcommunity.com/profiles/" + str(data.xuid)
