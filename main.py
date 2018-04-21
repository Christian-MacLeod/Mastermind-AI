import Player

def multiTest(runs):
    while True:
        Player.run(code_length, domain)
        runs -= 1
        if runs == 0:
            break


def guidedComparisonTest(runs):
    print("Running test comparing guided initial turns vs. unguided system\nRuns: {}\nAverage Attempts:".format(runs))
    turns = Player.competeGuided(code_length, domain)
    rolling_average_guided = [turns[1], 1]
    rolling_average_unguided = [turns[0], 1]
    for i in range(runs):
        turns = Player.competeGuided(code_length, domain)

        rolling_average_guided[1] += 1
        rolling_average_guided[0] += (turns[1] - rolling_average_guided[0]) / rolling_average_guided[1]

        rolling_average_unguided[1] += 1
        rolling_average_unguided[0] += (turns[0] - rolling_average_unguided[0]) / rolling_average_unguided[1]
    print("Guided: {} Unguided: {}".format(rolling_average_guided[0], rolling_average_unguided[0]))


def timedTest(runs, turn_limit):
    print("Running test with limited attempts\nRuns: {}\tAttempts: {}".format(runs, turn_limit))
    successes = 0
    failures = 0
    average_turns = 0

    for i in range(runs):
        trial = Player.competeTimed(code_length, domain, turn_limit, True)
        if trial[0]:
            successes += 1
        else:
            failures += 1
        if average_turns == 0:
            average_turns = trial[1]
        else:
            average_turns += (trial[1]-average_turns)/(successes+failures)
    print("Successes: {}\tFailures: {}\nAverage Attempts: {}".format(successes, failures, average_turns))

code_length = 5
domain = {i for i in range(8)}

#multiTest(100)
timedTest(1000, 10)
guidedComparisonTest(1000)