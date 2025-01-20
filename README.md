# Code Review Crew for GitHub Pull Request

Welcome to the CodeReviewCrewForGithubPullRequest project, powered by [crewAI](https://crewai.com). This project sets up a multi-agent AI system designed to perform comprehensive code reviews for GitHub pull requests.

## Project Overview

This crew consists of two main agents:

1. **Quick Review Assistant**: Provides rapid initial assessments of code changes and identifies basic patterns and potential issues in pull requests.
2. **Code Review Expert**: Analyzes code changes in detail and provides comprehensive review reports highlighting code quality issues and suggestions for improvements.

## Key Features

- Automated code analysis for GitHub Pull Requests
- Identification of related files and potential impacts
- Analysis of historically related Pull Requests
- Generation of detailed, markdown-formatted code review comments

## Installation

Ensure you have Python >=3.10 <=3.13 installed. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.
Follow the [installation guide for CrewAI](https://docs.crewai.com/docs/installation).

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

* Add your `OPENAI_API_KEY` to the `.env` file as we use gpt-4o-mini to perform fetching PRs, files, etc.
* Add your `ANTHROPIC_API_KEY` to the `.env` file - this project uses Anthropic's models for code review.

## Configuration

- `src/code_review_crew_for_github_pull_request/config/agents.yaml`: Define agent roles and configurations
- `src/code_review_crew_for_github_pull_request/config/tasks.yaml`: Specify tasks for code review process
- `src/code_review_crew_for_github_pull_request/crew.py`: Customize logic, tools, and arguments
- `src/code_review_crew_for_github_pull_request/main.py`: Add custom inputs for agents and tasks

## Usage

Run the code review crew:

```bash
crewai run
```

This command initializes the crew, assigns tasks, and generates a comprehensive code review report.

## Task Workflow

1. **Analyze Code Changes**: Evaluate modified files for quality issues and suggest improvements
2. **Find Related PRs**: Search for and analyze previous related pull requests
3. **Analyze Related Files**: Identify and analyze files functionally or logically related to the changes
4. **Generate Review Comment**: Synthesize insights into a comprehensive code review comment

## Support

For support or questions:
- Visit our [documentation](https://docs.crewai.com)
- Check our [GitHub ](https://github.com/crewAIInc)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Leverage the power of AI for efficient and thorough code reviews with this crew!
