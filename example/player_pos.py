from DemoParser import DemoParser
import player_pos_funcs as test

test.parser = DemoParser(demo_path=test.demo_path, ent="ALL")

test.parser.subscribe_to_event("parser_new_tick", test.print_player_positions)
test.parser.subscribe_to_event("gevent_begin_new_match", test.begin_new_match)
test.parser.subscribe_to_event("gevent_round_officially_ended", test.round_officially_ended)
test.parser.subscribe_to_event("gevent_round_freeze_end", test.round_freeze_end)

test.parser.parse()
