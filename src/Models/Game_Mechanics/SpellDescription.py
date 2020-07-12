class SpellDescription:
    name: str
    desc: [str]
    range: str
    components: [str]
    ritual: bool
    duration: str
    concentration: bool
    casting_time: str
    school: [str]
    level: str
    higher_level: [str]

    # def __init__(self, name, description, range, components, ritual, duration, concentration, castingTime, school):
    #     self.name = name
    #     self.description = description
    #     self.range = range
    #     self.components = components
    #     self.ritual = ritual
    #     self.duration = duration
    #     self.concentration = concentration
    #     self.casting_time = castingTime
    #     self.school = school

    def __init__(self, dictionary):
        self.__dict__.update(dictionary)

    # def init_from_json(self, json):
    #     self.name = json['name']
    #     self.description = json['description']
    #     self.range = json['range']
    #     self.components = json['components']
    #     self.ritual = json['ritual']
    #     self.duration = json['duration']
    #     self.concentration = json['concentration']
    #     self.casting_time = json['castingTime']
    #     self.school = json['school']
