import random

# A few definitions and classes
all_teams = []


class Team:

    def __init__(self, name):
        self._played = []
        self._name = name

    def get_name(self):
        return self._name

    def get_played_teams(self):
        return self._played

    def played_team(self, team):
        self._played.append(team)


# Make creator
# Get teams or preset
creator = input("Please put teams below, or a specific league (specify with l:) Separate different seasons with _s#\n")
if creator.__contains__("l:"):
    # TSL
    if creator == "l:TSL_s1":
        ascend = Team("Team Ascend")
        noble = Team("Noble United")
        ace = Team("Ace Gaming")
        outdone = Team("Outdone Movement")
        switch = Team("Switch Up Esports")
        tt6 = Team("Troll Team 6")
        projekt = Team("Projekt Crimson")
        immortal = Team("Immortal Gaming")
        gravity = Team("Gravity Esports")
        unity = Team("Unity Esports")
        lycus = Team("Lycus Empire")
        nova = Team("Nova Core")
        t303 = Team("303")
        fractured = Team("Fractured Memories")
        pantheon = Team("Pantheon")
        scc = Team("SCC Blue")
        full_send = Team("Full Send")
        yung = Team("Yung King")
        intervention = Team("Intervention Esports")
        luxx = Team("Luxxury Esports Academy")
        draak = Team("Draak Esports")
        efficiency = Team("Efficiency Gaming")
        darkside = Team("Darkside Gaming")
        zelos = Team("Zelos")
        sxd = Team("Shattered Dreams Esports")
        noctus = Team("NOCTUS")
        giants = Team("Sleeping Giants")
        vanity = Team("Team Vanity")
        mountain = Team("Iron Mountain")
        wwg = Team("War Wraiths Gaming")
        r1 = Team("1st rounders")
        finalshot = Team("Finalshot")

        # Matchday 1 VVVV
        gravity.played_team(intervention)
        intervention.played_team(gravity)
        nova.played_team(noble)
        noble.played_team(nova)
        unity.played_team(pantheon)
        pantheon.played_team(unity)
        ascend.played_team(wwg)
        wwg.played_team(ascend)
        outdone.played_team(luxx)
        luxx.played_team(outdone)
        tt6.played_team(full_send)
        full_send.played_team(tt6)
        switch.played_team(t303)
        t303.played_team(switch)
        projekt.played_team(efficiency)
        efficiency.played_team(projekt)
        fractured.played_team(zelos)
        zelos.played_team(fractured)
        lycus.played_team(sxd)
        sxd.played_team(lycus)
        scc.played_team(yung)
        yung.played_team(scc)
        # Echo X forfeits against draak
        giants.played_team(r1)
        r1.played_team(giants)
        # Matchday 2 VVVV
        intervention.played_team(switch)
        switch.played_team(intervention)
        noctus.played_team(scc)
        scc.played_team(noctus)
        r1.played_team(lycus)
        lycus.played_team(r1)
        giants.played_team(efficiency)
        efficiency.played_team(giants)
        # Echo X forfeits against Nova
        draak.played_team(full_send)
        full_send.played_team(draak)
        yung.played_team(tt6)
        tt6.played_team(yung)
        zelos.played_team(outdone)
        outdone.played_team(zelos)
        projekt.played_team(t303)
        t303.played_team(projekt)
        luxx.played_team(gravity)
        gravity.played_team(luxx)
        ascend.played_team(pantheon)
        pantheon.played_team(ascend)
        unity.played_team(noble)
        noble.played_team(unity)
        wwg.played_team(sxd)
        sxd.played_team(wwg)
        mountain.played_team(noctus)
        mountain.played_team(fractured)

        all_teams.append(ascend)
        all_teams.append(noctus)
        all_teams.append(fractured)
        all_teams.append(mountain)
        all_teams.append(wwg)
        all_teams.append(sxd)
        all_teams.append(unity)
        all_teams.append(noble)
        all_teams.append(pantheon)
        all_teams.append(gravity)
        all_teams.append(luxx)
        all_teams.append(t303)
        all_teams.append(projekt)
        all_teams.append(outdone)
        all_teams.append(zelos)
        all_teams.append(tt6)
        all_teams.append(yung)
        all_teams.append(draak)
        all_teams.append(full_send)
        all_teams.append(giants)
        all_teams.append(efficiency)
        all_teams.append(r1)
        all_teams.append(lycus)
        all_teams.append(scc)
        all_teams.append(intervention)
        all_teams.append(switch)
        all_teams.append(nova)
        all_teams.append(finalshot)

        print("All TSL season 1 teams added")

# Create schedule
matches = int(input("How many matches do you want to play? (Must be an integer)\n"))

for m in range(matches):
    pool = all_teams
    nums_used = []
    for t in range(int(len(pool)/2)):
        t1num = random.randint(0, len(pool)-1)
        while nums_used.__contains__(t1num):
            t1num = random.randint(0, len(pool) - 1)
        t1 = pool[t1num]
        nums_used.append(t1num)
        t2num = 0
        if not len(pool) == 0:
            t2num = random.randint(0, len(pool)-1)
        while t1.get_played_teams().__contains__(pool[t2num]) or nums_used.__contains__(t2num):
            t2num = random.randint(0, len(pool)-1)
        t2 = pool[t2num]
        nums_used.append(t2num)

        t1.played_team(t2)
        t2.played_team(t1)

        print(t1.get_name() + " is playing " + t2.get_name())
    print("Group", m+1, "done.")
