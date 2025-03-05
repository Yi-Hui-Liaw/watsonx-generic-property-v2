from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.property_agent.tools.custom_tool import UpdateCSV, RunSQL
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
    base_url="https://us-south.ml.cloud.ibm.com",
    params=parameters,
    project_id=os.getenv("WATSONX_PROJECT_ID", None),
    apikey=os.getenv("WATSONX_API_KEY", None),
)


@CrewBase
class ManagerCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    update_csv = UpdateCSV()
    run_sql = RunSQL()

    facts_tool = RagTool(
        description="Use this tool to extract facts related to the minh, zig or connaught property.",
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
            vectordb=dict(
                provider="chroma",
                config=dict(
                    dir=f'rag-db'
                )
            )
        ),
        # summarize=True,
    )
    facts_tool.add(data_type="directory", source="knowledge/rag")

    csv_tool = RagTool(
        description="Use this tool to extract stocks or unit related information from .csv files",
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
            vectordb=dict(
                provider="chroma",
                config=dict(
                    dir=f'csv-db'
                )
            )
        ),
    )
    csv_tool.add(data_type="directory", source="knowledge/csv")

    @agent
    def customer_service_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_service_agent"],
            llm=llm,
            allow_delegation=False,
            max_iter=2,
            verbose=True,
        )

    # @agent
    # def booking_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config["csv_agent"],
    #         llm=llm,
    #         allow_delegation=False,
    #         max_iter=2,
    #         verbose=True,
    #         tools=[self.update_csv],
    #     )

    @agent
    def csv_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["csv_agent"],
            llm=llm,
            allow_delegation=False,
            max_iter=2,
            verbose=True,
            tools=[self.update_csv],
        )
    
    @agent
    def sql_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["sql_agent"],
            llm=llm,
            allow_delegation=False,
            max_iter=2,
            verbose=True,
            tools=[self.run_sql],
        )

    @agent
    def rag_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["rag_agent"],
            llm=llm,
            allow_delegation=False,
            max_iter=2,
            verbose=True,
            tools=[self.facts_tool],
        )

    ########################### TASK ###########################
    @task
    def route_task(self) -> Task:
        return Task(
            config=self.tasks_config["route_task"],
        )

    @task
    def book_route(self) -> Task:
        return Task(
            config=self.tasks_config["book_route"],
        )

    @task
    def rag_converse(self) -> Task:
        return Task(
            config=self.tasks_config["rag_converse"],
        )

    @task
    def book_converse(self) -> Task:
        return Task(
            config=self.tasks_config["book_converse"],
        )

    @task
    def search_property_facts(self) -> Task:
        return Task(config=self.tasks_config["search_property_facts"])

    @task
    def search_property_database(self) -> Task:
        return Task(config=self.tasks_config["search_property_database"])
    
    @task
    def transform_query_sql(self) -> Task:
        return Task(config=self.tasks_config["transform_query_sql"])

    @task
    def extract_property_book(self) -> Task:
        return Task(config=self.tasks_config["extract_property_book"])

    @task
    def update_property_book(self) -> Task:
        return Task(config=self.tasks_config["update_property_book"])
    
    @task
    def summarize_booking(self) -> Task:
        return Task(config=self.tasks_config["summarize_booking"])

    @crew
    def crew(self, mode="route") -> Crew:
        """Creates the Healthhive crew"""
        if mode == "route":
            return Crew(
                agents=[self.customer_service_agent()],
                tasks=[self.route_task()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "property_facts":
            return Crew(
                agents=[self.rag_agent(), self.customer_service_agent()],
                tasks=[self.search_property_facts(), self.rag_converse()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "property_database":
            return Crew(
                agents=[self.sql_agent(), self.customer_service_agent()],
                tasks=[self.transform_query_sql(), self.search_property_database(), self.rag_converse()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "property_book":
            return Crew(
                agents=[self.customer_service_agent()],
                tasks=[self.book_route()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "property_book_converse":
            return Crew(
                agents=[self.customer_service_agent()],
                tasks=[self.book_converse()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == "property_book_update":
            return Crew(
                agents=[self.customer_service_agent(), self.csv_agent()],
                tasks=[self.extract_property_book(), self.update_property_book(), self.summarize_booking()],
                process=Process.sequential,
                verbose=True,
            )
