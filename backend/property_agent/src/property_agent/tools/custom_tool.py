import os
import json
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List

# class Appointment(BaseModel):
#     """Input schema for UpdateCSV."""

#     appointment: str = Field(..., description="JSON string of appointment information.")

class Query(BaseModel):
    requirements: str = Field(..., description="JSON string of user preferences like bedrooms, max_price")

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
        
# class RunSQL(BaseTool):
#     name: str = "run_sql"
#     description: str = (
#         "Use this tool to run SQL query to extract property information related to units."
#     )
#     args_schema: Type[BaseModel] = Query

#     def _run(self, sql_query: str) -> str:
#         # Implementation goes here
#         try:
#             print("Running sql query...")
#             con = sqlite3.connect("sql-db/property.db")
#             df = pd.read_sql(sql_query, con=con)

#             return df
#         except Exception as e:
#             return e

class RecommendProperty(BaseTool):
    name: str = "recommend_property"
    description: str = (
        "This tool recommends properties based on user preferences (e.g., number of bedrooms, price, size)."
    )
    args_schema: Type[BaseModel] = Query 

    def _run(self, requirements: str) -> str:
        preferences = json.loads(requirements)
        property_data = self.load_multiple_property_data("knowledge/json")
        matching_properties = self.filter_properties(preferences, property_data)

        if matching_properties:
            return json.dumps(matching_properties, indent=2)
        else:
            return "No matching properties found based on your preferences."

    def load_multiple_property_data(self, directory_path: str):
        all_property_data = []
        
        for filename in os.listdir(directory_path):
            if filename.endswith(".json"):
                with open(os.path.join(directory_path, filename), "r") as f:
                    property_data = json.load(f)
                    all_property_data.append(property_data)
        print(all_property_data)
        
        return all_property_data

    def filter_properties(self, preferences, property_data):
        matched_properties = []
        
        for property_json in property_data:
            for unit in property_json['project']['unit_types']:
                if self.is_match(preferences, unit):
                    matched_properties.append({
                        'property_name': property_json['project']['name'],
                        'unit': unit
                    })

        return matched_properties

    def is_match(self, preferences, unit):
        if 'bedrooms' in preferences and preferences['bedrooms'] > unit['configuration']['bedrooms']:
            return False
        if 'max_price' in preferences and float(preferences['max_price']) < float(unit['price'].replace("RM", "").replace(",", "")):
            return False
        
        return True
