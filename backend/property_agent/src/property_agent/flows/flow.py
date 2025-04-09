from pydantic import BaseModel
from typing import Any, Mapping, List
from crewai.flow import Flow, listen, start
from src.property_agent.crews.manager_crew.manager_crew import ManagerCrew
import json

class CollectState(BaseModel):
    route: str | None = None
    page_url: str | None = ""
    query: str | None = None
    inputs: List[Mapping[str, Any]] | None = []
    # matching_properties: List[Mapping[str, Any]] | None = []
    # inputs: str | None= ""

class RouterFlow(Flow[CollectState]):
    @start()
    def start(self):
        print("Starting the property recommender flow")
        self.state.route = "start"
        input_str =  "\n".join(
            [
                f"user: {c['u']}" if 'u' in c else f"assistant: {c['a']}" for c in self.state.inputs
            ]
        )
        self.state.inputs = input_str
        print("History inputs: ",self.state.inputs)

    # router still broken atm
    @listen(start)
    def route_task(self):
        #Routing aka planning task.
        result = (
            ManagerCrew().crew(mode='route').kickoff(inputs={"conversation": self.state.inputs})
        )
        result = str(result).strip()

        
        self.state.route = result
        print(f"Route task determined - '{self.state.route}'")

    # @listen(route_task)
    # def book_route_task(self):
    #     print(f"Update booking route - '{self.state.route}'")
    #     if self.state.route != 'property_book':
    #         return
        
    #     result = (
    #         ManagerCrew().crew(mode='property_book').kickoff(inputs={"conversation": self.state.inputs})
    #     )
    #     result = str(result).strip()
    #     result = 'property_book_converse' if result == 'false' else 'property_book_update'
    #     self.state.route = result 

    @listen(route_task)
    def recommend_property_task(self):
        print(f"Update property recommendation task - '{self.state.route}'")
        if self.state.route != 'property_recommender':
            return

        property_data = (
            ManagerCrew().crew(mode='retrieve_data').kickoff(inputs={"conversation": self.state.inputs})
        )

        print(f"Extracted data type - {type(property_data.raw)}")

        recommendation = (
            ManagerCrew().crew(mode='recommend_property').kickoff(inputs={
                "properties": property_data.raw
                })
        )

        result = (
            ManagerCrew().crew(mode='converse').kickoff(inputs={
                "conversation": self.state.inputs,
                "information": recommendation.raw,
                "context": "the information provided is the recommended properties. You are generating a reply to recommend to the user. You must not suggest or offer any service. You are merely recommending the right property."
                })
        )
        result = str(result.raw).strip()
        return result

    # @listen(book_route_task)
    # def run_task(self):
    #     print(f"Execute {self.state.route} task")
    #     result = (
    #             ManagerCrew()
    #             .crew(mode=self.state.route)
    #             .kickoff(
    #                 inputs={
    #                     "page_url": self.state.page_url,
    #                     "conversation": self.state.inputs,
    #                 }
    #             )
    #         )
    #     self.state.query = str(result)

    # @listen(recommend_property_task)
    # def complete_task(self):
    #     print("complete conversation")
    #     if self.state.matching_properties:
    #         return self.state.matching_properties
    #     return """Sorry. We could not understand your query. Could please rephrase your question?"""