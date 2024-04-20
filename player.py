class Player:
    gold = 50

    @classmethod
    def earn_gold(cls, amount=1):
        cls.gold += amount

    @classmethod
    def can_buy(cls, amount : int):
        return cls.gold >= amount

    @classmethod
    def spend_gold(cls, amount : int ) :
        cls.gold -= amount

