import requests

url = "https://disease-info-api.herokuapp.com/diseases"


def get_disease_info(disease_name):
    return requests.get(url+f"/{disease_name}").json()






