class Character:
    name: str
    armor_class: int
    passive_perception: int
    max_hit_points: int
    current_hit_points: int

    def __init__(self, name, ac=0, pp=0, max_hp=0):
        self.name = name

    def set_max_hp(self, new_hp):
        self.max_hit_points = new_hp

    def update_current_hp(self, operand: str, amount: int):
        if operand == "+":
            self.current_hit_points += amount
        else:
            self.current_hit_points -= amount
        if self.current_hit_points > self.max_hit_points:
            self.current_hit_points = self.max_hit_points

            