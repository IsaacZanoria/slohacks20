import os
import json
from pprint import pprint

def get_refined_loads():
    with open(r"C:\Users\izack\Downloads\namus_api.json", "r") as file:
        loads = json.load(file)


    # pprint(loads)
    refined_loads = {}

    for missing_individ in loads:

        try:
            refined_loads[missing_individ["fields"]["idformatted"]] = {
                    "firstname": missing_individ["fields"]["firstname"],
                    "lastname": missing_individ["fields"]["lastname"],
                    "raceethnicity": missing_individ["fields"]["raceethnicity"],
                    "dateoflastcontact": missing_individ["fields"]["dateoflastcontact"],
                    "cityoflastcontact": missing_individ["fields"]["cityoflastcontact"],
                    "stateoflastcontact": missing_individ["fields"]["statedisplaynameoflastcontact"],
                    "currentage": missing_individ["fields"]["currentageto"],
                    "gender":  missing_individ["fields"]["gender"],
                    "link": missing_individ["fields"]["link"],
            }
        except KeyError:
            del refined_loads[missing_individ["fields"]["idformatted"]]
            pass
    return refined_loads