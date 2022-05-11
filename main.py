from flask import Flask, request, jsonify
import re
import long_responses as long
import disease_detector as dd
import disease_info as info
import health_tips as tips

continue_bot = True


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1  # matched words

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def collect_symptoms_and_detect_disease():
    patient_symptoms_list = input("Enter the symptoms separated by comma:"
                                  "\n(Type 'back' to get back to chat)\n").split(", ")
    if 'back' in patient_symptoms_list:
        return
    continue_asking_symptoms = True
    while continue_asking_symptoms and 'back' not in patient_symptoms_list:
        print("The entered symptoms are: ")
        for i in range(0, len(patient_symptoms_list)):
            print(f"{i + 1}: {patient_symptoms_list[i]}")
        continue_symptoms = input("\nDo you have any other symptoms?(Yes/No/Back): ").lower()
        if continue_symptoms == 'back':
            return
        if continue_symptoms in ["yes", "y"]:
            symptoms = input("Enter the remaining symptoms separated by comma: ").split(", ")
            patient_symptoms_list.extend(symptoms)
        else:
            continue_asking_symptoms = False
    print("The final list of symptoms are: ")
    for i in range(0, len(patient_symptoms_list)):
        print(f"{i + 1}. {patient_symptoms_list[i]}")
    print("\n")
    dd.detect_disease(patient_symptoms_list)


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo', 'wassup', 'sup'], single_response=True)
    response('See you, take care of your health!', ['bye', 'goodbye', 'good bye', 'tata', '👋'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing', '?'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('That\'s awesome😎', ['I am', 'I\'m', 'good'], required_words=['good'])
    response('Nice to hear😍', ['I am', 'I\'m', 'well'], required_words=['well'])
    response('Sounds great😎', ['I am', 'I\'m', 'fine'], required_words=['fine'])
    response(long.R_ASSIST,
             ['I', 'need', 'a', 'help'], required_words=['help'])
    response(long.ASK_SYMPTOMS, ['I', 'have', 'some', 'health',  'issues'],
             required_words=['health', 'issues'])
    response(long.ASK_SYMPTOMS, ['I', 'have', 'a', 'fever'])
    response(long.ASK_PROBLEM, ['I', 'have', 'problem'])
    response(long.ASK_SYMPTOMS, ['I', 'have', 'headache'])
    response("Please mind your words!!", ['You', 'are', 'an', 'idiot'], required_words=['you', 'idiot'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing the response system
# while continue_bot:
#     user_message = input('You: ')
#     if 'about' in user_message or 'info' in user_message or 'information' in user_message:
#         disease = input("Which disease you want to know about?.. ")
#         info.show_disease_info(disease)
#         continue
#     if 'tip' in user_message or 'advice' in user_message:
#         print(f"{tips.get_tip()['title']}: {tips.get_tip()['content'].strip()}")
#         continue
#     doc_bot_response = get_response(user_message)
#     print('Doc-Bot: ' + doc_bot_response)
#     if doc_bot_response == long.ASK_SYMPTOMS:
#         collect_symptoms_and_detect_disease()

app = Flask(__name__)


@app.route('/general_reply', methods=['GET'])
def general_bot_reply():
    d={}
    client_query = request.args['Query']
    if 'tip' in client_query or 'advice' in client_query:
        d['Query'] = f"{tips.get_tip()['title']}: {tips.get_tip()['content'].strip()}"
        return jsonify(d)
    doc_bot_response = get_response(client_query)
    d['Query'] = doc_bot_response
    return jsonify(d)


@app.route('/DiseaseInfoApi', methods=['GET'])
def disease_info_query():
    disease = request.args['disease']
    return info.get_disease_info(disease)


@app.route('/PredictDiseaseApi', methods=['GET'])
def predict_disease():
    d = {}
    symptoms = request.args['symptoms']
    symptoms_list = symptoms.split(", ")
    d['predicted_results'] = dd.detect_disease(symptoms_list)
    return jsonify(d)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')