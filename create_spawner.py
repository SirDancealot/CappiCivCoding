from custom_items import CUSTOM_ITEMS
item = "{{id:\"{0}\",Count:{1}, tag:{{{2}}}}}"
entity = "{{entity:{{id:{0},PersistenceRequired:1,HandItems:[{1},{2}],ArmorItems :[{3},{4},{5},{6}],HandDropChances:[{7}],ArmorDropChances:[{8}]}}}}"
spawn_potentiel = "{{weight:{0},data:{1}}}"

enchantment = "{{lvl: {0}s, id:\"{1}\"}}"
tool_enchantment = "Enchantments:[{0}]"
book_enchantment = "StoredEnchantments:[{0}]"

yes_options = ["y", "yes"]
no_options = ["n", "no"]
unstackables = ["axe","shovel","sword","hoe","horn","trident","shield","helmet","chestplate","leggings","boots","totem_of_undying","carved_pumpkin","jack","fishing","a_stick","_bucket"]


def inp(message):
    return input(message).lower().strip().replace(" ", "_")

def generate_enchantment(is_book: bool) -> str:
    do_enchantment = inp("should it be enchanted?: (y/N)") in yes_options
    if not do_enchantment:
        return ""
    
    enchantment_list = []

    number_of_enchantments = int(inp("how many enchantments should it have?: "))
    for i in range(number_of_enchantments):

        enchantment_id = inp("enchantment id: ")
        level = inp("enchantment level: ")

        enchantment_list.append(enchantment.format(level, enchantment_id))

    if is_book:
        return book_enchantment.format(",".join(enchantment_list))
    else:
        return tool_enchantment.format(",".join(enchantment_list))



def generate_item(message):
    print("-"*20)
    print(message)
    item_id = inp("item id: ")
    if item_id == "":
        return "{}", 0.0
    item_count = 1 if any([unstackable in item_id for unstackable in unstackables]) else inp("item count: ")
    drop_chance = float(inp("drop chance (in percent): "))
    drop_chance = (drop_chance / 100.0) if drop_chance != "" else 0.0
    if item_id in CUSTOM_ITEMS.keys():
        return CUSTOM_ITEMS.get(item_id).format(item_count), drop_chance
    enchantments = generate_enchantment(item_id == "enchanted_book")
    return item.format(item_id, item_count, enchantments), drop_chance

def generate_entity(message):
    hand_drop_chances = [0.0, 0.0]
    armor_drop_chances = [0.0, 0.0, 0.0, 0.0]
    print(message)
    entity_id = inp("entity id: ")
    main_hand, hand_drop_chances[0] = generate_item("main-hand item")
    off_hand, hand_drop_chances[1] = generate_item("off-hand item")
    boots, armor_drop_chances[0] = generate_item("boots")
    leggings, armor_drop_chances[1] = generate_item("leggings")
    chestplate, armor_drop_chances[2] = generate_item("chestplate")
    helmet, armor_drop_chances[3] = generate_item("helmet") 
    return entity.format(entity_id, main_hand, off_hand, boots, leggings, chestplate, helmet, ",".join(list(map(lambda chance: f"{chance}f", hand_drop_chances))), ",".join(list(map(lambda chance: f"{chance}f", armor_drop_chances))))


def generate_spawn_potential(message: str):
    print(message)
    monster = generate_entity(f"Generate monser for {message}")
    weight = inp("monster weight: ")
    return spawn_potentiel.format(weight,monster)





initial_spawn_delay = inp("Initial spawn delay: ")
min_spawn_delay = inp("minimum spawn delay: ")
max_spawn_delay = input("max spawn delay: ")
spawn_count = inp("spawn count: ")

first_monster = generate_entity("first spawn")
multiple_monsters = inp("should there be multiple monsters? (y/N) ")



monster_list = []

if multiple_monsters in yes_options:
    continue_spawning_first_monster = not (inp("should the first monster continue spawning? (Y/n) ") in no_options)
    num_monsters = int(input("Additional number of monsters: "))
    if continue_spawning_first_monster:
        first_monster_weight = inp("first monster weight: ")
        monster_list.append(spawn_potentiel.format(first_monster_weight,first_monster))
    for i in range(num_monsters):
        print("-"*20)
        monster_list.append(generate_spawn_potential(f"Generating potential number {i}")) 






spawner = f"setblock ~ ~1 ~ spawner{{SpawnData:{first_monster},Delay:{initial_spawn_delay},SpawnPotentials:[{','.join(monster_list)}],MinSpawnDelay:{min_spawn_delay},MaxSpawnDelay:{max_spawn_delay},SpawnCount:{spawn_count}}} replace"

print(spawner)