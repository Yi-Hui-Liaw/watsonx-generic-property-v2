
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from src.healthcare.tools.custom_tool import UpdateCSV
from crewai_tools import DirectorySearchTool #CSVSearchTool,TXTSearchTool,DirectoryReadTool

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
    csv_updater = UpdateCSV()

    facts_tool= DirectorySearchTool(
        csv="knowledge/rag",
        description="Use this tool to extract propery facts from .txt files.",
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
        ),
    )

    database_tool= DirectorySearchTool(
        csv="knowledge/csv/DirectorySearchTool.csv",
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
        ),
    )

    @agent
    def customer_service_agent(self) -> Agent:
        return Agent(config=self.agents_config["customer_service_agent"], 
                     llm=llm, 
                     allow_delegation=False, 
                     max_iter=2, 
                     verbose=True)
    @agent
    def booking_agent(self) -> Agent:
        return Agent(config=self.agents_config["customer_service_agent"], 
                     llm=llm, 
                     allow_delegation=False, 
                     max_iter=2, 
                     verbose=True,
                     tools=[self.csv_updater])

    @agent
    def csv_agent(self) -> Agent:
        return Agent(config=self.agents_config["csv_agent"], 
                     llm=llm, 
                     allow_delegation=False, 
                     max_iter=2, 
                     verbose=True,
                     tools=[self.database_tool])
    
    @agent
    def rag_agent(self) -> Agent:
        return Agent(config=self.agents_config["rag_agent"], 
                     llm=llm, 
                     allow_delegation=False, 
                     max_iter=2, 
                     verbose=True, 
                     tools=[self.facts_tool])

########################### TASK ###########################
    @task
    def route_task(self) -> Task:
        return Task(
            config=self.tasks_config["route_task"],
        )
    
    @ConditionalTask
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
    def extract_property_book(self) -> Task:
        return Task(config=self.tasks_config["extract_property_book"])

    @task
    def update_property_book(self) -> Task:
        return Task(config=self.tasks_config["update_property_book"])

    @crew
    def crew(self, mode='route') -> Crew:
        """Creates the Healthhive crew"""
        if mode == 'route':
            return Crew(
                agents=[self.customer_service_agent()],
                tasks=[self.route_task()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == 'property_facts':
            return Crew(
                agents=[self.rag_agent(),self.customer_service_agent()],
                tasks=[self.search_property_facts(), self.rag_converse()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == 'property_database':
            return Crew(
                agents=[self.csv_agent(), self.customer_service_agent()],
                tasks=[self.search_property_database(), self.rag_converse()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == 'property_book':
            return Crew(
                agents=[self.customer_service_agent()],
                tasks=[self.book_route()],
                process=Process.sequential,
                verbose=True,
            )
        elif mode == 'property_book_converse':
            return Crew(
                agents=[self.customer_service_agent()],
                tasks=[self.book_converse()],
                process=Process.sequential,
                verbose=True,
            )   
        elif mode == 'property_book_update':
            return Crew(
                agents=[self.booking_agent()],
                tasks=[self.extract_property_book(), self.update_property_book()],
                process=Process.sequential,
                verbose=True,
            )