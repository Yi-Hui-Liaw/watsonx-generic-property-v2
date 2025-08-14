from pydantic import BaseModel
from typing import Any, Mapping, List
from crewai.flow import Flow, listen, start
from src.property_agent.crews.manager_crew.manager_crew import ManagerCrew
import ast, json
from src.property_agent.tools.custom_tool import QueryProperty, Query

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

    # @listen(route_task)
    # def property_facts_task(self):
    #     print(f"Running property facts task - '{self.state.route}'")
    #     if self.state.route != 'property_facts':
    #         return

    #     result = (
    #         ManagerCrew().crew(mode='facts').kickoff(inputs={
    #             "conversation": self.state.inputs
    #         })
    #     )

    #     response = (
    #         ManagerCrew().crew(mode='converse').kickoff(inputs={
    #             "conversation": self.state.inputs,
    #             "information": result.raw,
    #             "context": "You are providing factual information about the property based on the user's query. Only mention facts such as tenure, property type, land title, or special features. If no facts are found, inform the user respectfully."
    #         })
    #     )

    #     return str(response.raw).strip()

    @listen(route_task)
    def recommend_property_task(self):
        print(f"Running task - '{self.state.route}'")
        if self.state.route == 'property_recommender':
            data_fields = ast.literal_eval((
                ManagerCrew().crew(mode='retrieve_data_field').kickoff(inputs={"conversation": self.state.inputs})
            ).raw)
            print(f"Extracted data field - {data_fields}")
            #property_data = load_properties(ast.literal_eval(data_fields.raw))
            tool = QueryProperty()
            # search_result = (
            #     ManagerCrew().crew(mode='retrieve_es_properties').kickoff(inputs={
            #         "conversation": self.state.inputs
            #     })
            # )
            properties = tool._run(self.state.inputs, data_fields)

            recommendation = (
                ManagerCrew().crew(mode='recommend_property').kickoff(inputs={
                    "conversation": self.state.inputs,
                    "properties": properties
                    })
            )

            result = (
                ManagerCrew().crew(mode='converse').kickoff(inputs={
                    "conversation": self.state.inputs,
                    "information": recommendation.raw,
                    "context": "the information provided is the recommended properties. You are generating a reply to recommend to the user. You must not suggest or offer any service. You are merely recommending the right property. Make sure to mention the name of the recommended properties."
                    })
            )
            result = str(result.raw).strip()

        elif self.state.route == 'property_facts':
            result = (
                ManagerCrew().crew(mode='facts').kickoff(inputs={
                    "conversation": self.state.inputs
                })
            )

            response = (
                ManagerCrew().crew(mode='converse').kickoff(inputs={
                    "conversation": self.state.inputs,
                    "information": result.raw,
                    "context": "You are providing factual information about the property based on the user's query. Only mention facts such as tenure, property type, land title, or special features. If no facts are found, inform the user respectfully."
                })
            )

            result = str(response.raw).strip()
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