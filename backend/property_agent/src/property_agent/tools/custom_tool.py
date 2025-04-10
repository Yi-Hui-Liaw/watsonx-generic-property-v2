import os
import json
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List
from crewai import LLM
from crewai_tools import ScrapeWebsiteTool

# class Appointment(BaseModel):
#     """Input schema for UpdateCSV."""

#     appointment: str = Field(..., description="JSON string of appointment information.")


class Query(BaseModel):
    requirements: str = Field(
        ..., description="JSON string of user preferences like bedrooms, max_price"
    )

class DataFields(BaseModel):
    data_fields: List[str] = Field(
        ..., description="list of data fields in string required for recommendations."
    )

# class UpdateCSV(BaseTool):
#     name: str = "csv_update"
#     essential_keys: List[str] = ['name','phone_number','property_unit_id']
#     description: str = (
#         "This is used to update csv using pandas based on provided dictionary. The keys in the dictionary will be determine to which columns or csv updated."
#     )
#     args_schema: Type[BaseModel] = Appointment

#     def _run(self, appointment: str) -> str:
#         print("Updating CSV")
#         info = json.loads(appointment)
#         print("Extracted information - ",info)
#         missing_keys = [ x for x in info.keys() if x not in self.essential_keys]
#         print("Missing information - ",missing_keys)
#         # Implementation goes here
#         try:

#             #Update user csv
#             appt_csv_path = "knowledge/csv/appointment.csv"
#             appt_df = pd.read_csv(appt_csv_path)
#             print(f"Updating patient, patient row - {appt_df.shape[0]}")

#             # columns - patient_id,patient_name,age,email,phone
#             appt_df.loc[len(appt_df)] = [info['name'], info['phone_number'], info['property_unit_id']]
#             appt_df.to_csv(appt_csv_path, index=False)
#             print(f"Appoinment's updated, appt row - {appt_df.shape[0]}")

#             return "Appointment csv has been updated."
#         except Exception as e:
#             return e
def load_properties(data_fields):
    # prop_dir = "./knowledge/json"
    # files = os.listdir(prop_dir)
    # match_prop = []
    # for f in files:
    #     print(f"loading {f}")
    #     with open(os.path.join(prop_dir, f), 'r') as jf:
    #         properties = json.load(jf)
    #         temp_prop = {k:v for k,v in properties['project'].items() if k in data_fields}
    #         match_prop.append(temp_prop)
    #         print(f"Match properties - {len(match_prop)}") 
    tool = ScrapeWebsiteTool(website_url='https://www.uemsunrise.com')
    property_data = tool.run()
    print(property_data)
    return property_data


class RetrievePropertyData(BaseTool):
    name: str = "retrieve property data"
    description: str = (
        "Use this tool to retrieve property data using data fields."
    )
    args_schema: Type[BaseModel] = DataFields



    def _run(self, data_fields: list[str]) -> List[dict]:
        print(f"Exracting {len(data_fields)} data fields")
        print(data_fields)
        # Implementation goes here
        data_fields = data_fields + ['project_name','concept'] # name and concept is a must for model to make a better decision
        
        try:
            properties = load_properties(data_fields)
            return properties
        except Exception as e:
            return e

class RecommendProperty(BaseTool):
    name: str = "recommend_property"
    description: str = "This tool recommends properties based on user preferences (e.g., number of bedrooms, price, size)."
    args_schema: Type[BaseModel] = Query

    def _run(self, requirements: str) -> str:
        preferences = json.loads(requirements)

        property_data = self.load_multiple_property_data("knowledge/json")

        prompt = self.create_prompt(preferences, property_data)

        recommendations = self.get_llm_response(prompt)

        return recommendations

    def load_multiple_property_data(self, directory_path: str):
        all_property_data = []

        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                with open(os.path.join(directory_path, filename), "r") as f:
                    property_data = json.load(f)
                    all_property_data.append(property_data)

        return all_property_data

    def create_prompt(self, preferences, property_data):
        prompt = f"""
        I need your help to recommend properties based on the following user preferences and available properties:
        
        User Preferences: 
        - Bedrooms: {preferences.get("bedrooms", "N/A")}
        - Max Price: {preferences.get("max_price", "N/A")}
        
        Available Properties:
        {json.dumps(property_data, indent=2)}
        
        Please recommend properties that match the user's preferences.
        """

        return prompt


    def get_llm_response(self, prompt: str) -> str:
        parameters = {"decoding_method": "greedy", "max_new_tokens": 500}

        llm = LLM(
            model="watsonx/meta-llama/llama-3-3-70b-instruct",
            base_url="https://jp-tok.ml.cloud.ibm.com",
            params=parameters,
            project_id=os.getenv("WATSONX_PROJECT_ID", None),
            apikey=os.getenv("WATSONX_API_KEY", None),
        )
        # To be completed
        # try:
        #     response = 
        #     if response and "choices" in response:
        #         generated_text = response["choices"][0].get(
        #             "text", "No recommendations found."
        #         )
        #         return generated_text
        #     else:
        #         return "Error: No response text available."

        # except Exception as e:
        #     return f"Error: {str(e)}"
