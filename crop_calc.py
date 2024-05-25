import os
import json
''',daysToMaturity, seedPrice, maxHarvest, sellPricePerHarvest, daysToRegrow, season'''
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
        #make a loop that stores the seed properties inside variables
        #then use the variables to calculate the gold per day/month
        #something like self.daysToMaturity and etcetera

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
        CC.populate_variables(seed_name=seed_name)
        growing_days = self.daysToMaturity + ((self.maxHarvest - 1) * self.daysToRegrow)
        minimum_gold_per_day = ((self.maxHarvest * self.sellPricePerHarvest) - self.seedPrice) / growing_days
        return minimum_gold_per_day
    
    ### DIFFERENTIATE SEEDS THAT REGROW FROM SEEDS THAT DONT REGROW, THE INCOME CALCULATION CHANGES FOR EACH
    def net_income_per_month(self, seed_name, quantityOfPlantedSeeds):
        CC.populate_variables(seed_name=seed_name)
        net_gold_per_month = ((quantityOfPlantedSeeds * self.sellPricePerHarvest) - (self.seedPrice * quantityOfPlantedSeeds)) * (28 // self.daysToMaturity) 
        return net_gold_per_month
    
    def gross_income_per_month(self, seed_name, quantityOfPlantedSeeds):
        CC.populate_variables(seed_name=seed_name)
        gross_gold_per_moth = ((quantityOfPlantedSeeds * self.sellPricePerHarvest)) * (28 // self.daysToMaturity)
        return gross_gold_per_moth

if __name__ == "__main__":
    CC = Crops_calculator()
gold_day = CC.gold_per_day("potato")
net_gold_month = CC.net_income_per_month("coffee", 30)
gross_gold_month = CC.gross_income_per_month("coffee", 30)
print(f"Gold per day ~= {gold_day}")
print(f"Net income per month ~= {net_gold_month}")
print(f"Gross income per moth: {gross_gold_month}")


