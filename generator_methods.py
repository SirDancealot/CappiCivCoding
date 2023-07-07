from custom_items import CUSTOM_ITEMS

YES_OPTIONS = ["y", "yes"]
NO_OPTIONS = ["n", "no"]
un_stack_ables = ["potion","axe","shovel","sword","hoe","horn","trident","shield","helmet","chestplate","leggings","boots","totem_of_undying","carved_pumpkin","jack","fishing","a_stick","_bucket"]


def inp(message):
    return input(message).lower().strip().replace(" ", "_")

enchantment = "{{lvl: {0}s, id:\"{1}\"}}"
tool_enchantment = "Enchantments:[{0}]"
book_enchantment = "StoredEnchantments:[{0}]"
def generate_enchantment(is_book: bool, force_enchant: bool = None, num_enchants: int|None = None) -> str:
    do_enchantment = force_enchant if force_enchant is not None else inp("should it be enchanted?: (y/N)") in YES_OPTIONS
    if not do_enchantment:
        return ""
    
    enchantment_list = []

    number_of_enchantments = num_enchants if num_enchants else int(inp("how many enchantments should it have?: "))
    for i in range(number_of_enchantments):

        enchantment_id = inp("enchantment id: ")
        level = inp("enchantment level: ")

        enchantment_list.append(enchantment.format(level, enchantment_id))

    if is_book:
        return book_enchantment.format(",".join(enchantment_list))
    else:
        return tool_enchantment.format(",".join(enchantment_list))



item = "{{id:\"{0}\",Count:{1}, tag:{{{2}}}}}"
horn = "{{id: \"goat_horn\", tag: {{instrument: {0}_goat_horn}}, Count: 1}}"
potion = "{{id: \"potion\", tag: {{Potion:{0}}}, Count: 1}}"
sus_stew = "{{id: \"suspicious_stew\", tag:{{Effects:[{{EffectId:{0}, EffectDuration:{1}}}]}}, Count: {2}}}"
def generate_item(message: str, get_drop_chance: bool = False, item_id = None, item_count = None, do_enchantment: bool|None = None, number_enchants: int|None = None):
    print("-"*20)
    print(message)
    item_id = item_id if item_id else inp("item id: ")
    if item_id == "":
        return "{}", 0.0
    item_count = item_count if item_count else (1 if any([un_stack_able in item_id for un_stack_able in un_stack_ables]) else inp("item count: "))
    drop_chance = 0.0
    if get_drop_chance:
        drop_chance = float(inp("drop chance (in percent): "))
        drop_chance = (drop_chance / 100.0) if drop_chance != "" else 0.0
    if item_id in CUSTOM_ITEMS.keys():
        if not get_drop_chance:
            return CUSTOM_ITEMS.get(item_id).format(item_count)
        return CUSTOM_ITEMS.get(item_id).format(item_count), drop_chance
    elif item_id == "horn":
        horn_type = inp("Horn type: ")
        if not get_drop_chance:
            return horn.format(horn_type)
        return horn.format(horn_type), drop_chance
    elif item_id == "potion":
        potion_effect = inp("Potion effect: ")
        if not get_drop_chance:
            return potion.format(potion_effect)
        return potion.format(potion_effect), drop_chance
    elif item_id in ['s_stew', 'sus_stew', 'suspicious_stew']:
        effect_id = inp("stew effect id: ")
        effect_duration = inp("Duration of effect (in ticks):")
        if not get_drop_chance:
            return sus_stew.format(effect_id, effect_duration, item_count)
        return sus_stew.format(effect_id, effect_duration, item_count), drop_chance
    enchantments = generate_enchantment(item_id == "enchanted_book", do_enchantment, number_enchants)
    if not get_drop_chance:
        return item.format(item_id, item_count, enchantments)
    return item.format(item_id, item_count, enchantments), drop_chance

entity = "{{entity:{{id:{0},PersistenceRequired:1,HandItems:[{1},{2}],ArmorItems :[{3},{4},{5},{6}],HandDropChances:[{7}],ArmorDropChances:[{8}]}}}}"
def generate_entity(message):
    hand_drop_chances = [0.0, 0.0]
    armor_drop_chances = [0.0, 0.0, 0.0, 0.0]
    print(message)
    entity_id = inp("entity id: ")
    main_hand, hand_drop_chances[0] = generate_item("main-hand item", True)
    off_hand, hand_drop_chances[1] = generate_item("off-hand item", True)
    boots, armor_drop_chances[0] = generate_item("boots", True)
    leggings, armor_drop_chances[1] = generate_item("leggings", True)
    chestplate, armor_drop_chances[2] = generate_item("chestplate", True)
    helmet, armor_drop_chances[3] = generate_item("helmet", True) 
    return entity.format(entity_id, main_hand, off_hand, boots, leggings, chestplate, helmet, ",".join(list(map(lambda chance: f"{chance}f", hand_drop_chances))), ",".join(list(map(lambda chance: f"{chance}f", armor_drop_chances))))


spawn_potential = "{{weight:{0},data:{1}}}"
def generate_spawn_potential(message: str):
    print(message)
    monster = generate_entity(f"Generate monser for {message}")
    weight = inp("monster weight: ")
    return spawn_potential.format(weight,monster)