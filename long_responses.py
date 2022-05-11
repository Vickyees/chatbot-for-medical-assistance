import random

R_EATING = "I don't like eating anything because I'm a bot obviously!"
R_ADVICE = "If I were you, I would go to the internet and type exactly what you wrote there!"
R_ASSIST = "Don\'t worry! I\'m here for you always. Just say what is your problem!🤔"
ASK_SYMPTOMS = "May I know your symptoms🙄"
ASK_PROBLEM = "problem with? do you have any health issues...?"


def unknown():
    response = ["Could you please re-phrase that? ",
                "...",
                "Something strange🤔",
                "What does that mean?"][
        random.randrange(4)]
    return response