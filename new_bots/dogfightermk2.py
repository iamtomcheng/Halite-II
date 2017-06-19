import common


def dogfighter():
    my_tag, map_size, initial_map, log = yield "Dogfighter Mark II"

    while True:
        game_map = yield
        command_queue = []

        for ship in game_map.ships[my_tag].values():
            if ship.docked == "docked" and game_map.planets[ship.planet].remaining_production == 0:
                command_queue.append(common.undock(ship))
                continue

            if ship.docked != "undocked":
                continue

            planets = game_map.planets.values()
            sort_key = lambda planet: common.distance(ship, planet)
            found_planet = False
            for planet in sorted(planets, key=sort_key):
                if planet.owned or planet.remaining_production == 0:
                    continue

                # Prevent multiple ships from converging on the same planet
                planet.owned = True

                angle, distance = common.orient_towards(ship, planet)
                if common.can_dock(ship, planet):
                    command_queue.append(common.dock(ship, planet))
                else:
                    command_queue.append(common.move_to(ship, angle, 1))

                found_planet = True

                break

            if found_planet:
                continue

            # No planet to go towards
            for player, ships in game_map.ships.items():
                if player == my_tag:
                    continue

                found_enemy = False

                for enemy in sorted(
                        ships.values(),
                        key=lambda enemy: common.distance(ship, enemy)):
                    angle, distance = common.orient_towards(ship, enemy)
                    # Only move closer to get into attack range
                    if distance > 10:
                        command_queue.append(common.move_to(ship, angle, 3))
                    elif distance > 5:
                        command_queue.append(common.move_to(ship, angle, 2))
                    elif distance > 3:
                        command_queue.append(common.move_to(ship, angle, 1))

                    found_enemy = True
                    break

                if found_enemy:
                    break

        yield command_queue

common.run_bot(dogfighter)