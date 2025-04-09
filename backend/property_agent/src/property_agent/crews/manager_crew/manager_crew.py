from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.property_agent.tools.custom_tool import RetrievePropertyData
from crewai_tools import (
    RagTool,
)
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# Parameters
parameters = {"decoding_method": "greedy", "max_new_tokens": 500}
llm = LLM(
    model="watsonx/meta-llama/llama-3-3-70b-instruct",
    base_url="https://jp-tok.ml.cloud.ibm.com",
    params=parameters,
    project_id=os.getenv("WATSONX_PROJECT_ID", None),
    apikey=os.getenv("WATSONX_API_KEY", None),
)


@CrewBase
class ManagerCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    # update_csv = UpdateCSV()
    RetrievePropertyTool = RetrievePropertyData()

    facts_tool = RagTool(
        description="Use this tool to extract facts related to the ABC Residence, Lumenh or The Nexus One property from .json files.",
        config=dict(
            llm=dict(
                provider="ollama",  # or google, openai, anthropic, llama2, ...
                config=dict(
                    model="llama3",
                    base_url="http://0.0.0.0:11434",
                    # temperature=0.5,
                    # top_p=1,
                    # stream=true,
                ),
            ),
            embedder=dict(
                provider="ollama",  # or openai, ollama, ...
                config=dict(
                    model="mxbai-embed-large",
                    # task_type="retrieval_document",
                    # title="Embeddings",
                ),
            ),
            vectordb=dict(provider="chroma", config=dict(dir=f"rag-db")),
        ),
        # summarize=True,
    )
    facts_tool.add(data_type="directory", source="knowledge/rag")

    # csv_tool = RagTool(
    #     description="Use this tool to extract stocks or unit related information from .csv files",
    #     config=dict(
    #         llm=dict(
    #             provider="ollama",  # or google, openai, anthropic, llama2, ...
    #             config=dict(
    #                 model="llama3",
    #                 base_url="http://0.0.0.0:11434",
    #                 # temperature=0.5,
    #                 # top_p=1,
    #                 # stream=true,
    #             ),
    #         ),
    #         embedder=dict(
    #             provider="ollama",  # or openai, ollama, ...
    #             config=dict(
    #                 model="mxbai-embed-large",
    #                 # task_type="retrieval_document",
    #                 # title="Embeddings",
    #             ),
    #         ),
    #         vectordb=dict(provider="chroma", config=dict(dir=f"csv-db")),
    #     ),
    # )
    # csv_tool.add(data_type="directory", source="knowledge/csv")

    @agent
    def customer_service_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_service_agent"],
            llm=llm,
            allow_delegation=False,
            max_iter=2,
            verbose=True,
        )

    @agent
    def search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["search_agent"],
            llm=llm,
            allow_delegation=False,
            max_iter=2,
            verbose=True,
            tools=[self.RetrievePropertyTool],
        )

    @agent
    def recommend_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["recommend_agent"],
            llm=llm,
            allow_delegation=False,
            max_iter=2,
            verbose=True,
        )

    ########################### TASK ###########################
    @task
    def route_task(self) -> Task:
        return Task(
            config=self.tasks_config["route_task"],
        )

    @task
    def search_property_facts(self) -> Task:
        return Task(config=self.tasks_config["search_property_facts"])

    @task
    def search_property_database(self) -> Task:
        return Task(config=self.tasks_config["search_property_database"])

    @task
    def recommend_property(self) -> Task:
        return Task(config=self.tasks_config["recommend_property"])

    @task
    def search_converse(self) -> Task:
        return Task(config=self.tasks_config["search_converse"])
    
    @task
    def converse(self) -> Task:
        return Task(config=self.tasks_config["converse"])
    
    @task
    def retrieve_data(self) -> Task:
        return Task(config=self.tasks_config["retrieve_data"])
    
    @task
    def match_data_field(self) -> Task:
        return Task(config=self.tasks_config["match_data_field"])
    
    ########################### CREW ###########################

    @crew
    def crew(self, mode="route") -> Crew:
        """Creates the Property Agent crew"""
        if mode == "route":
            return Crew(
                agents=[self.customer_service_agent()],
                tasks=[self.route_task()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "facts":
            return Crew(
                agents=[self.search_agent(), self.customer_service_agent()],
                tasks=[self.search_property_facts()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "search_database":
            return Crew(
                agents=[self.sql_agent(), self.customer_service_agent()],
                tasks=[
                    self.search_property_database(),
                    self.search_converse(),
                ],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "recommend_property":
            return Crew(
                agents=[self.recommend_agent(),],
                tasks=[self.recommend_property()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "retrieve_data":
            return Crew(
                agents=[self.search_agent()],
                tasks=[self.match_data_field(), self.retrieve_data()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "converse":
            return Crew(
                agents=[ self.customer_service_agent()],
                tasks=[self.converse()],
                process=Process.sequential,
                verbose=True,
            )