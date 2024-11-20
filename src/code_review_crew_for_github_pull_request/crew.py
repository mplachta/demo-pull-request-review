from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
import os

@CrewBase
class CodeReviewCrewForGithubPullRequestCrew():
    """CodeReviewCrewForGithubPullRequest crew"""

    @agent
    def code_retriever(self) -> Agent:
        return Agent(
            config=self.agents_config['code_retriever'],
        )

    @agent
    def code_review_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['code_review_expert'],
        )


    @task
    def retrieve_modified_files_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieve_modified_files_task'],
            tools=[ScrapeWebsiteTool()],
        )

    @task
    def analyze_code_changes_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_code_changes_task'],
            tools=[],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the CodeReviewCrewForGithubPullRequest crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
