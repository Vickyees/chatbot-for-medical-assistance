import csv

file = "dis_sym_dataset_norm.csv"
disease_dict = {}


def detect_disease(patient_symptoms_list):

    with open(file, 'r', encoding='utf8') as data:
        for disease in csv.DictReader(data):
            symptoms_list = []
            for k, v in disease.items():
                if v == 1 or v == '1':
                    symptoms_list.append(k)
            disease_dict[disease['label_dis']] = symptoms_list

    patient_disease_common_symptoms = []
    for disease, disease_symptoms in disease_dict.items():
        common_symptoms = []
        for patient_symptom in patient_symptoms_list:
            if patient_symptom in disease_symptoms:
                common_symptoms.append(patient_symptom)
        common_percentage = round((len(common_symptoms) / len(patient_symptoms_list) * 100), 2)
        # print(f"{len(common_percentage)} / {len(patient_symptom)}")
        if len(common_symptoms) > 0:
            patient_disease_common_symptoms.append(
                {'disease': disease, 'common_symptoms': common_symptoms, 'common_percentage': common_percentage})

    count = 0
    disease_percentage_list = []
    for i in sorted(patient_disease_common_symptoms, key=lambda i: i['common_percentage'], reverse=True):
        if count < 10:
            disease_percentage_list.append(f"{count+1}. {i['disease']} --> probability: {i['common_percentage']}%")
            print(f"{count+1}. {i['disease']} --> probability: {i['common_percentage']}%")
        count += 1

    print("\nThe above list of diseases and probabilites may not be accurate,\nit is solely predicted based on the symptoms given\nand so it is not recommended to take any medicines\nor treatments without the real doctor's consulation.")
    return disease_percentage_list