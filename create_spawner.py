from generator_methods import inp, generate_entity, generate_spawn_potential, YES_OPTIONS as yes_options, NO_OPTIONS as no_options

spawn_potential = "{{weight:{0},data:{1}}}"

initial_spawn_delay = inp("Initial spawn delay: ")
min_spawn_delay = inp("minimum spawn delay: ")
max_spawn_delay = inp("max spawn delay: ")
spawn_count = inp("spawn count: ")

first_monster = generate_entity("first spawn")
multiple_monsters = inp("should there be multiple monsters? (y/N) ")

monster_list = []

if multiple_monsters in yes_options:
    continue_spawning_first_monster = inp("should the first monster continue spawning? (Y/n) ") not in no_options
    num_monsters = int(inp("Additional number of monsters: "))
    if continue_spawning_first_monster:
        first_monster_weight = inp("first monster weight: ")
        monster_list.append(spawn_potential.format(first_monster_weight,first_monster))
    for i in range(num_monsters):
        print("-"*20)
        monster_list.append(generate_spawn_potential(f"Generating potential number {i}")) 

spawner = f"setblock ~ ~1 ~ spawner{{SpawnData:{first_monster},Delay:{initial_spawn_delay},SpawnPotentials:[{','.join(monster_list)}],MinSpawnDelay:{min_spawn_delay},MaxSpawnDelay:{max_spawn_delay},SpawnCount:{spawn_count}}} replace"

print(spawner)