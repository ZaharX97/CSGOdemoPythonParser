from DemoParser import DemoParser
import example.round_stats_functions as my


path = r"C:\Users\Zahar\Desktop\asd\demo.dem"
dump_path = r"C:\Users\Zahar\Desktop\asd\demodump.txt"

x = DemoParser(path, dump=dump_path, ent="NONE")

x.subscribe_to_event("parser_start", my.new_demo)
x.subscribe_to_event("gevent_player_team", my.player_team)
x.subscribe_to_event("gevent_player_death", my.player_death)
x.subscribe_to_event("gevent_player_spawn", my.player_spawn)
x.subscribe_to_event("gevent_bot_takeover", my.bot_takeover)
x.subscribe_to_event("gevent_begin_new_match", my.begin_new_match)
x.subscribe_to_event("gevent_round_end", my.round_end)
x.subscribe_to_event("gevent_round_officially_ended", my.round_officially_ended)
x.subscribe_to_event("parser_update_pinfo", my.update_pinfo)
x.subscribe_to_event("cmd_dem_stop", my.cmd_dem_stop)
x.subscribe_to_event("parser_demo_finished_print", my.print_match_stats)

x.parse()
