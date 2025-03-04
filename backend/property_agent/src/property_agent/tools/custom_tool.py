from typing import Type
import sqlite3
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List
import json
import pandas as pd

class Appointment(BaseModel):
    """Input schema for UpdateCSV."""

    appointment: str = Field(..., description="JSON string of appointment information.")

class Query(BaseModel):
    """Input schema for RunSQL."""

    sql_query: str = Field(..., description="SQL string following schema provided")

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
        
class RunSQL(BaseTool):
    name: str = "run_sql"
    description: str = (
        "Use this tool to run SQL query to extract property information related to units."
    )
    args_schema: Type[BaseModel] = Query

    def _run(self, sql_query: str) -> str:
        # Implementation goes here
        try:
            print("Running sql query...")
            con = sqlite3.connect("sql-db/property.db")
            df = pd.read_sql(sql_query, con=con)

            return df
        except Exception as e:
            return e