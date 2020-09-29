import random
import decimal
import sys
import math

# A few definitions and classes

highest_elo = 0
lowest_elo = 0

decimal.getcontext().prec = 100

all_teams = []


# Function to calculate the Probability
def Probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))


# Function to calculate Elo rating
# K is a constant.
# d determines whether
# Player A wins or Player B.
def EloRating(Ra, Rb, K, t1, t2):
    bias = 1
    bias2 = 1

    # To calculate the Winning
    # Probability of Player B
    Pb = Probability(Ra, Rb)

    # To calculate the Winning
    # Probability of Player A
    Pa = Probability(Rb, Ra)

    if Pa > Pb:
        bias = ((t1 + t2) / 2) / Pa
        bias2 = 7 / Pa
    elif Pa < Pb:
        bias = ((t1 + t2) / 2) / Pb
        bias2 = 7 / Pb
    elif Pa == Pb:
        bias = ((t1 + t2) / 2) / Pa
        bias2 = 6 / Pa

    print("Expected score:", round(Pa*bias2, 0), "-", round(Pb*bias2, 0))

    # Updating the Elo Ratings
    Ra = Ra + K * ((t1-t2) - (bias*Pa - bias*Pb))
    Rb = Rb + K * ((t2-t1) - (bias*Pb - bias*Pa))

    print("Updated Ratings: Ra =", round(Ra, 6), " Rb =", round(Rb, 6))

    return [Ra, Rb]


class Match:
    t1result = 0
    t2result = 0
    result = "0-0"

    def __init__(self, teams2, ID_):
        self.teams = teams2
        self.id = ID_

    def get_teams(self):
        return self.teams

    def get_result(self):
        return self.result

    def set_result(self, result):
        self.result = result
        self.t1result = int(result.split("-")[0])
        self.t2result = int(result.split("-")[1])

    def set_elos(self):
        print(self.teams[0].get_name() + " (", self.teams[0].get_elo(), ") v " + self.teams[1].get_name() + " (", self.teams[1].get_elo(), ") -> ", self.t1result, " - ", self.t2result, sep="")

        t1_score = self.t1result
        t2_score = self.t2result

        if t1_score - t2_score == 0:
            return

        rat_A = self.teams[0].get_elo()
        rat_B = self.teams[1].get_elo()

        rat_new = EloRating(rat_A, rat_B, 25, t1_score, t2_score)

        # Team calculations
        self.teams[0].manual_elo(rat_new[0])
        self.teams[1].manual_elo(rat_new[1])

    def exp_result(self):
        bias = 7
        bias2 = 7

        # To calculate the Winning
        # Probability of Player B
        Pb = Probability(self.teams[0].get_elo(), self.teams[1].get_elo())

        # To calculate the Winning
        # Probability of Player A
        Pa = Probability(self.teams[1].get_elo(), self.teams[0].get_elo())

        if Pa > Pb:
            for i in range(bias * 2):
                if round(Pa * bias, 0) == 7:
                    break
                else:
                    bias += 1
            bias2 = 7 / Pa
        elif Pa < Pb:
            for i in range(bias2 * 2):
                if round(Pb * bias2, 0) == 7:
                    break
                else:
                    bias2 += 1
            bias = 7 / Pb
        elif Pa == Pb:
            bias = 6 / Pb
            bias2 = 6 / Pa

        print(self.teams[0].get_name() + " v. " + self.teams[1].get_name() + "; Expected score:", round(Pa * bias, 0), "-", round(Pb * bias2, 0))

    def get_id(self):
        return self.id


class Team:
    elo = 1500

    def __init__(self, name):
        self._played = []
        self._name = name

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_played_teams(self):
        return self._played

    def played_team(self, team):
        self._played.append(team)

    def get_elo(self):
        return self.elo

    def add_elo(self, change):
        self.elo += change

    def reset_elo(self):
        self.elo = 100

    def manual_elo(self, new_elo):
        self.elo = new_elo


def sort_elo(to_sort_t):
    all_sorted_teams = []

    to_sort = to_sort_t

    for pl_to_add in range(len(to_sort)):  # Loop over all players to be added
        if pl_to_add == 0:  # Check if list is empty
            all_sorted_teams.append(to_sort[pl_to_add])
            continue
        for al_added in range(len(all_sorted_teams)):  # Loop over players in scoreboard
            if to_sort[pl_to_add].get_elo() > all_sorted_teams[al_added].get_elo():
                # Has more points than this player so add him
                all_sorted_teams.insert(al_added, to_sort[pl_to_add])
                break
            if al_added + 1 >= len(all_sorted_teams):
                all_sorted_teams.append(to_sort[pl_to_add])
                break

    return all_sorted_teams


def progress_bar(current, total, name, bar_length=100):
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\r{0: <{1}} [{2}]{3}%".format(name, 20, arrow + spaces, (percent * 100).__round__(3)))
    sys.stdout.flush()
    if current == total:
        sys.stdout.write('\n\n')


def play_match(team1, team2, result, id, played=True):
    if played:
        team1.played_team(team2)
        team2.played_team(team1)
        match = Match([team1, team2], id)
        match.set_result(result)
        match.set_elos()
    else:
        match = Match([team1, team2], id)
        match.exp_result()


def sim_match(team1, team2, matches_to_play):
    t1_res = 0
    t2_res = 0
    ac = 2000
    for acc in range(ac):
        for i in range(matches_to_play):
            bias = 7
            bias2 = 7

            r = (random.random() - random.random()) * 1.6

            # To calculate the Winning
            # Probability of Player B
            Pb = Probability(team1.get_elo(), team2.get_elo()) + r

            # To calculate the Winning
            # Probability of Player A
            Pa = Probability(team2.get_elo(), team1.get_elo()) - r

            if Pa > Pb:
                for i in range(bias * 2):
                    if round(Pa * bias, 0) == 7:
                        break
                    else:
                        bias += 1
                bias2 = 7 / Pa
            elif Pa < Pb:
                for i in range(bias2 * 2):
                    if round(Pb * bias2, 0) == 7:
                        break
                    else:
                        bias2 += 1
                bias = 7 / Pb
            elif Pa == Pb:
                bias = 6 / Pb
                bias2 = 6 / Pa

            if round(Pa * bias, 0) > round(Pb * bias2, 0):
                t1_res += 1
            else:
                t2_res += 1
    print(team1.get_name() + " v " + team2.get_name() + "; Total win %s: ", (t1_res*100)/(matches_to_play*ac), "% - ", (t2_res*100)/(matches_to_play*ac), "%", sep="")


# Make creator
# Get teams or preset
creator = input("Please put teams below, or a specific league (specify with l:) Separate different seasons with _s#\n")
if creator.__contains__("l:"):
    # TSL
    if creator == "l:TSL_s1":
        achieve = Team("Team Achieve")
        infamous = Team("Infamous United")
        outdone = Team("Outdone Movement")  # REPLACED
        hc = Team("HC eSports")
        tt6 = Team("Troll Team 6")
        projekt = Team("Projekt Crimson")
        gravity = Team("Gravity eSports")
        unity = Team("Unity eSports")
        lycus = Team("Lycus Empire")
        nova = Team("Nova Core")
        t303 = Team("303")
        fractured = Team("Fractured Memories")  # REPLACED
        pantheon = Team("Pantheon")
        scc = Team("SCC Blue")
        fullsend = Team("Full Send")
        anax = Team("ANAX eSports")
        intervention = Team("Intervention eSports")
        luxx = Team("Luxxury eSports Academy")
        draak = Team("Draak eSports")
        eff = Team("Efficiency Gaming")
        zelos = Team("Zelos")
        sxd = Team("Shattered Dreams eSports")
        giants = Team("Sleeping Giants")
        talentless = Team("Talentless eSports")
        dgen = Team("dGeneration eSports")
        cursed = Team("Cursed Ascension")
        frosty = Team("Frosty eSports")  # LOOKING FOR REPLACEMENT
        finalshot = Team("Finalshot")
        imperium = Team("Imperium Academy")  # REPLACEMENT (OUTDONE)
        phantom = Team("Phantom Legion")  # REPLACEMENT (FRAC)

        all_teams2 = []

        # PRESEASON

        # Matchday 1 VVVV

        play_match(intervention, gravity, "7-4", 0)
        play_match(nova, infamous, "7-4", 1)
        play_match(pantheon, unity, "7-4", 2)
        play_match(dgen, achieve, "7-3", 3)
        play_match(tt6, fullsend, "7-5", 4)
        play_match(projekt, eff, "8-7", 5)
        play_match(zelos, fractured, "7-4", 6)
        play_match(lycus, sxd, "7-5", 7)
        play_match(scc, anax, "7-3", 8)

        # Matchday 2 VVVV

        play_match(eff, giants, "7-1", 9)
        play_match(fullsend, draak, "7-5", 10)
        play_match(outdone, zelos, "7-1", 11)
        play_match(t303, projekt, "8-6", 12)
        play_match(luxx, gravity, "7-3", 13)
        play_match(infamous, unity, "7-5", 14)
        play_match(dgen, sxd, "7-2", 15)
        play_match(fractured, talentless, "7-1", 16)

        # Matchday 3 VVVV

        play_match(lycus, nova, "7-2", 17)
        play_match(pantheon, sxd, "7-4", 18)
        play_match(intervention, talentless, "7-2", 19)
        play_match(fractured, outdone, "7-2", 20)
        play_match(gravity, dgen, "8-6", 21)
        play_match(zelos, unity, "7-0", 22)
        play_match(projekt, luxx, "7-2", 23)
        play_match(achieve, eff, "7-5", 24)
        play_match(fullsend, giants, "7-3", 25)
        play_match(draak, anax, "8-7", 26)
        play_match(scc, finalshot, "8-6", 27)

        # Matchday 4 VVVV

        play_match(anax, pantheon, "8-7", 28)
        play_match(nova, fullsend, "7-2", 29)
        play_match(cursed, giants, "7-5", 30)
        play_match(dgen, talentless, "7-5", 31)
        play_match(gravity, unity, "7-4", 32)
        play_match(achieve, sxd, "7-4", 33)
        play_match(intervention, draak, "7-4", 34)
        play_match(eff, luxx, "7-0", 35)
        play_match(lycus, projekt, "7-5", 36)
        play_match(tt6, outdone, "7-4", 37)

        # GROUPS:
        # Group 1
        play_match(intervention, tt6, "7-5", 38)
        play_match(lycus, fractured, "7-5", 38)
        play_match(intervention, fractured, "0-0", 38)
        play_match(lycus, tt6, "8-6", 38)
        play_match(intervention, lycus, "7-2", 38)
        play_match(fractured, tt6, "0-0", 38)
        # Group 2
        play_match(zelos, scc, "0-0", 38)
        play_match(dgen, t303, "0-0", 38)
        play_match(t303, zelos, "7-2", 38)
        play_match(dgen, scc, "7-4", 38)
        play_match(zelos, dgen, "0-0", 38)
        play_match(t303, scc, "7-1", 38)
        # Group 3
        play_match(nova, pantheon, "7-0", 38)
        play_match(infamous, eff, "7-1", 38)
        play_match(eff, nova, "7-1", 38)
        play_match(infamous, pantheon, "7-2", 38)
        play_match(nova, infamous, "0-0", 38)
        play_match(pantheon, eff, "7-5", 38)
        # Group 4
        play_match(projekt, draak, "7-1", 38)
        play_match(gravity, fullsend, "7-5", 38)
        play_match(projekt, fullsend, "7-5", 38)
        play_match(draak, gravity, "7-4", 38)
        play_match(projekt, gravity, "7-5", 38)
        play_match(fullsend, draak, "7-4", 38)
        # Group 5
        play_match(cursed, luxx, "7-5", 38)
        play_match(achieve, outdone, "0-0", 38)
        play_match(outdone, cursed, "7-4", 38)
        play_match(achieve, luxx, "7-5", 38)
        play_match(cursed, achieve, "7-2", 38)
        play_match(luxx, outdone, "0-0", 38)
        # Group 6
        play_match(unity, anax, "7-4", 38)
        play_match(talentless, finalshot, "0-0", 38)
        play_match(unity, talentless, "7-4", 38)
        play_match(anax, finalshot, "7-1", 38)
        play_match(unity, finalshot, "8-6", 38)
        play_match(anax, talentless, "7-4", 38)
        # Group 7
        play_match(sxd, frosty, "8-6", 38)
        play_match(giants, hc, "0-0", 38)
        play_match(sxd, hc, "0-0", 38)
        play_match(frosty, giants, "7-3", 38)
        play_match(sxd, giants, "7-0", 38)
        play_match(hc, frosty, "7-0", 38)

        # WEEK 4
        print("WEEK 4 VVV")

        fullsend.set_name("Flagship Blue")

        play_match(intervention, luxx, "7-1", 0)
        play_match(lycus, unity, "7-3", 0)
        play_match(tt6, t303, "4-7", 0)
        play_match(phantom, sxd, "7-2", 0)
        play_match(zelos, achieve, "0-0", 0)
        play_match(dgen, anax, "5-7", 0)
        play_match(scc, eff, "8-6", 0)
        play_match(nova, cursed, "7-5", 0)
        play_match(infamous, draak, "7-5", 0)
        play_match(pantheon, gravity, "6-8", 0)
        play_match(projekt, frosty, "0-0", 0)
        play_match(fullsend, talentless, "7-5", 0)
        play_match(imperium, giants, "0-0", 0)
        play_match(finalshot, hc, "5-7", 0)

        # WEEK 5 -> fair matches
        print("WEEK 5 VVV")

        play_match(intervention, scc, "7-4", 0)
        play_match(lycus, dgen, "7-3", 0)
        play_match(tt6, zelos, "7-0", 0)
        play_match(phantom, t303, "5-7", 0)
        play_match(nova, gravity, "5-7", 0)
        play_match(infamous, projekt, "2-7", 0)
        play_match(eff, luxx, "7-2", 0)
        play_match(pantheon, achieve, "0-0", 0)
        play_match(fullsend, cursed, "7-3", 0)
        play_match(draak, imperium, "0-0", 0)
        play_match(anax, frosty, "8-7", 0, False)
        play_match(unity, hc, "3-7", 0)
        play_match(talentless, sxd, "3-7", 0)
        play_match(finalshot, giants, "0-0", 0)

        # WEEK 6 -> fair matches
        print("WEEK 6 VVV")

        play_match(intervention, zelos, "7-5", 0)
        play_match(lycus, t303, "7-0", 0)
        play_match(tt6, scc, "0-0", 0)
        play_match(phantom, dgen, "0-0", 0)
        play_match(nova, imperium, "7-4", 0)
        play_match(infamous, cursed, "7-8", 0)
        play_match(eff, draak, "7-0", 0)
        play_match(pantheon, fullsend, "6-8", 0)
        play_match(projekt, achieve, "0-0", 0)
        play_match(gravity, luxx, "0-0", 0)
        play_match(anax, sxd, "3-7", 0)
        play_match(unity, giants, "7-4", 0)
        play_match(talentless, hc, "0-0", 0)
        play_match(finalshot, frosty, "0-0", 0, False)

        print("")
        print("")
        print("")
        print("PLAYOFFS VVV")
        print("QUARTERFINALS VVV")
        sim_match(projekt, imperium, 1)
        play_match(projekt, imperium, "8-6", 0)
        sim_match(t303, sxd, 1)
        play_match(t303, sxd, "7-1", 0)
        sim_match(nova, anax, 1)
        play_match(nova, anax, "7-8", 0)
        print("SEMIFINALS VVV")
        sim_match(projekt, intervention, 3)
        play_match(projekt, intervention, "7-1", 0)
        play_match(projekt, intervention, "6-8", 0)
        play_match(projekt, intervention, "7-5", 0)
        sim_match(t303, anax, 3)
        # 303 HEAVY FAVORITES
        play_match(t303, anax, "0-0", 0, False)
        play_match(t303, anax, "0-0", 0, False)
        play_match(t303, anax, "0-0", 0, False)
        print("FINALS VVV")
        sim_match(t303, projekt, 5)

        all_teams2.append(achieve)
        all_teams2.append(finalshot)
        all_teams2.append(phantom)
        # all_teams2.append(frosty) Team left
        all_teams2.append(fullsend)
        # all_teams2.append(tt6) Team left
        all_teams2.append(talentless)
        all_teams2.append(t303)
        # all_teams2.append(luxx) Team left
        all_teams2.append(lycus)
        all_teams2.append(dgen)
        all_teams2.append(draak)
        all_teams2.append(cursed)
        all_teams2.append(sxd)
        all_teams2.append(scc)
        all_teams2.append(giants)
        all_teams2.append(gravity)
        all_teams2.append(eff)
        all_teams2.append(nova)
        all_teams2.append(imperium)
        all_teams2.append(infamous)
        all_teams2.append(intervention)
        all_teams2.append(anax)
        all_teams2.append(pantheon)
        all_teams2.append(projekt)
        all_teams2.append(unity)
        all_teams2.append(hc)
        all_teams2.append(zelos)

        all_teams2 = sort_elo(all_teams2)

        highest_elo = all_teams2[0].get_elo()
        lowest_elo = all_teams2[len(all_teams2) - 1].get_elo

        print("\nAll TSL season 1 teams added")

        all_teams = all_teams2

# Create schedule
matches = int(input("How many matches do you want to play? (Must be an integer)\n"))

all_sorted_teams2 = sort_elo(all_teams)
for teams in range(len(all_sorted_teams2)):
    print("#", teams + 1, " is " + all_sorted_teams2[teams].get_name() + " with an elo of ",
          int(all_sorted_teams2[teams].get_elo()), sep="")

for m in range(matches):
    pool = all_teams
    nums_used = []
    for t in range(int(len(pool) / 2)):
        t1num = random.randint(0, len(pool) - 1)
        while nums_used.__contains__(t1num):
            t1num = random.randint(0, len(pool) - 1)
        t1 = pool[t1num]
        nums_used.append(t1num)
        t2num = 0
        if not len(pool) == 0:
            t2num = random.randint(0, len(pool) - 1)
        while t1.get_played_teams().__contains__(pool[t2num]) or nums_used.__contains__(t2num):
            t2num = random.randint(0, len(pool) - 1)
        t2 = pool[t2num]
        nums_used.append(t2num)

        t1.played_team(t2)
        t2.played_team(t1)

        print(t1.get_name() + " is playing " + t2.get_name())
    print("Week", m + 4, "done.")
