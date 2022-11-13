import random

from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units


class WorkerRushBot(BotAI):
    async def on_step(self, iteration: int):
        main_base = self.townhalls.first
        if not main_base:
            return



        if self.structures(UnitTypeId.SPAWNINGPOOL).amount == 0:
            if self.already_pending(UnitTypeId.SPAWNINGPOOL) < 1 and self.already_pending(UnitTypeId.VESPENEGEYSER) < 2:
                if self.can_afford(UnitTypeId.EXTRACTOR):
                    # May crash if we dont have any drones
                    for gaz in self.vespene_geyser.closer_than(10, main_base):
                        drone: Unit = self.workers.closest_to(gaz)
                        drone.build_gas(gaz)
            else:
                print(f"{self.can_afford(UnitTypeId.SPAWNINGPOOL)} iteration: {iteration}")
                if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                    print("Create Pool!")
                    self.units(UnitTypeId.DRONE).closest_to(main_base)(AbilityId.ZERGBUILD_SPAWNINGPOOL,
                                                                       main_base.position.towards(
                                                                           self.game_info.map_center, 5))

        # Saturate gas
        for a in self.gas_buildings:
            if a.assigned_harvesters < a.ideal_harvesters:
                w: Units = self.workers.closer_than(10, a)
                if w:
                    w.random.gather(a)

run_game(maps.get("AcropolisLE"), [
    Bot(Race.Zerg, WorkerRushBot()),
    Computer(Race.Protoss, Difficulty.Medium)],
         realtime=True
         )
