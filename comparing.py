import main_application

GREATER_COLOUR = "green"
LESSER_COLOUR = "red"


class CompareStats:
    def __init__(self, pWidget1, pWidget2):
        self.player1Widget = pWidget1
        self.player2Widget = pWidget2

        self.p1_skillWidgets = self.player1Widget.getSkillWidgets()
        self.p2_skillWidgets = self.player2Widget.getSkillWidgets()

    def compareSkills(self):
        for skillName in self.p1_skillWidgets:

            p1_skillWidget = self.p1_skillWidgets[skillName]
            p2_skillWidget = self.p2_skillWidgets[skillName]

            p1_skillValue = int(p1_skillWidget.getSkillLevel())
            p2_skillValue = int(p2_skillWidget.getSkillLevel())

            if p1_skillValue > p2_skillValue:
                p1_skillWidget.setBackground(GREATER_COLOUR)
                p2_skillWidget.setBackground(LESSER_COLOUR)
            elif p1_skillValue < p2_skillValue:
                p1_skillWidget.setBackground(LESSER_COLOUR)
                p2_skillWidget.setBackground(GREATER_COLOUR)
            else:
                p1_skillWidget.setBackground(main_application.BACKGROUND_COLOR)
                p2_skillWidget.setBackground(main_application.BACKGROUND_COLOR)

    def clearCompareColours(self):
        for skillName in zip(self.p1_skillWidgets, self.p2_skillWidgets):
            p1_skillWidget = self.p1_skillWidgets[skillName]
            p2_skillWidget = self.p2_skillWidgets[skillName]

            p1_skillWidget.setBackground(main_application.BACKGROUND_COLOR)
            p2_skillWidget.setBackground(main_application.BACKGROUND_COLOR)
