import json


class Crops_calculator:
    def __init__ (self,name=None ,daysToMaturity=None, seedPrice=None, maxHarvest=None, sellPricePerHarvest=None, daysToRegrow=None, season=None):
        print("Hello!\n")
        self.name = name
        self.daysToMaturity = daysToMaturity
        self.seedPrice = seedPrice
        self.maxHarvest = maxHarvest
        self.sellPricePerHarvest = sellPricePerHarvest
        self.daysToRegrow = daysToRegrow
        self.season = season

    def populate_variables(self, seed_name):
        with open('seeds.json', 'r') as file_seed:
            data = json.load(file_seed)

        self.name = seed_name
        seeds_db = data['seeds']

        for seed in seeds_db:
            if seed['name'] == self.name:
                self.daysToMaturity = seed['days_to_maturity']
                self.seedPrice = seed['seed_price']
                self.maxHarvest = seed['max_harvest']
                self.sellPricePerHarvest = seed['sell_price_per_harvest']
                self.daysToRegrow = seed['days_to_regrow']
                self.season = seed['season']

    def gold_per_day(self, seed_name):
        self.populate_variables(seed_name=seed_name)
        growing_days = self.daysToMaturity + ((self.maxHarvest - 1) * self.daysToRegrow)
        minimum_gold_per_day = ((self.maxHarvest * self.sellPricePerHarvest) - self.seedPrice) / growing_days
        formatted = "{:.2f}".format(minimum_gold_per_day)
        return formatted
    
    def net_income_per_month(self, seed_name, quantityOfPlantedSeeds):
        self.populate_variables(seed_name=seed_name)
        if self.maxHarvest == 1:
            net_gold_per_month = ((quantityOfPlantedSeeds * self.sellPricePerHarvest) - (self.seedPrice * quantityOfPlantedSeeds)) * (28 // self.daysToMaturity) 
        elif self.maxHarvest > 1:
            net_gold_per_month = (quantityOfPlantedSeeds * (self.sellPricePerHarvest * self.maxHarvest)) - (self.seedPrice * quantityOfPlantedSeeds)
        return net_gold_per_month
    
    def gross_income_per_month(self, seed_name, quantityOfPlantedSeeds):
        self.populate_variables(seed_name=seed_name)
        if self.maxHarvest == 1:
            gross_gold_per_moth = ((quantityOfPlantedSeeds * self.sellPricePerHarvest)) * (28 // self.daysToMaturity)
        elif self.maxHarvest > 1:
            gross_gold_per_moth = (quantityOfPlantedSeeds * (self.sellPricePerHarvest * self.maxHarvest))
        return gross_gold_per_moth

    def needed_gold(self, seed_name, quantityOfSeeds):
        self.populate_variables(seed_name=seed_name)
        cost = quantityOfSeeds * self.seedPrice
        return cost

if __name__ == "__main__":
    CC = Crops_calculator()


