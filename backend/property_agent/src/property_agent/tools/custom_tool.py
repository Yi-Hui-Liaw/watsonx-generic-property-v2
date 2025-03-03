from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List
import json
import pandas as pd

class Appointment(BaseModel):
    """Input schema for MyCustomTool."""

    appointment: str = Field(..., description="JSON string of appointment information.")


class UpdateCSV(BaseTool):
    name: str = "csv_update"
    essential_keys: List[str] = ['name','phone_number','property_unit_id']
    description: str = (
        "This is used to update csv using pandas based on provided dictionary. The keys in the dictionary will be determine to which columns or csv updated."
    )
    args_schema: Type[BaseModel] = Appointment

    def _run(self, appointment: str) -> str:
        print("Updating CSV")
        info = json.loads(appointment)
        print("Extracted information - ",info)
        missing_keys = [ x for x in info.keys() if x not in self.essential_keys]
        print("Missing information - ",missing_keys)
        # Implementation goes here
        try:
            
            #Update user csv
            appt_csv_path = "knowledge/csv/appointment.csv"
            appt_df = pd.read_csv(appt_csv_path)
            print(f"Updating patient, patient row - {appt_df.shape[0]}")
            
            # columns - patient_id,patient_name,age,email,phone
            appt_df.loc[len(appt_df)] = [info['name'], info['phone_number'], info['property_unit_id']]
            appt_df.to_csv(appt_csv_path, index=False)
            print(f"Appoinment's updated, appt row - {appt_df.shape[0]}")

            return "All csv has been updated."
        except Exception as e:
            return e