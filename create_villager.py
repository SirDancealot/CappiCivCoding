from generator_methods import generate_item, YES_OPTIONS, inp

horn = "{{id: \"goat_horn\", tag: {{instrument: {0}_goat_horn}}, Count: 1}}"
item = "{{id:\"{0}\",Count:{1}}}"


villager_profession = input("Villager profession: ")
villager_level = input("Villager level: ")
villager_type = input("Villager biome: ")

num_trades = int(input("Number of trades: "))
trade_list = []


trade = "{{buy:{0},sell:{1},rewardExp:0b,maxUses:9999999}}"
dual_trade = "{{buy:{0},buyB:{1},sell:{2},rewardExp:0b,maxUses:9999999}}"

for i in range(num_trades):
    do_dual_trade = input("dual-trade?: [y/N]").lower()

    if do_dual_trade in YES_OPTIONS:
        item_1 = generate_item("generating buy item 1", False)
        item_2 = generate_item("generating buy item 2", False)
        sell_item = generate_item("generating sell item", False, can_be_shulker=True)
        trade_list.append(dual_trade.format(item_1, item_2, sell_item))
    else:
        buy_item = generate_item("generating buy item")
        sell_item = generate_item("generating sell item", can_be_shulker=True)
        trade_list.append(trade.format(buy_item, sell_item))

trade_string = ",".join(trade_list)
rotation = input("villager rotation: ")
villager = f"summon villager ~-0.5 ~1.5 ~-0.5 {{VillagerData: {{profession: \"{villager_profession}\", level: {villager_level}, type: \"{villager_type}\"}}, Invulnerable: 1, Silent: 1, PersistenceRequired: 1, NoAI: 1, Offers: {{Recipes: [{trade_string}]}}, Rotation:[{rotation}f,0f]}}"

print(villager)