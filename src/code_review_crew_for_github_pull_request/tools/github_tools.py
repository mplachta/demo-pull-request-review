from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
from github import Github
from typing import List, Optional
import os

class FetchPRFilesInput(BaseModel):
    """Input schema for FetchPRFilesTool."""
    pr_patch_url: str = Field(..., description="URL of the PR patch file to analyze")

class FetchPRFilesTool(BaseTool):
    name: str = "Fetch PR Modified Files"
    description: str = "Retrieves the patch and contents of all modified files in a GitHub pull request"
    args_schema: Type[BaseModel] = FetchPRFilesInput

    def _run(self, pr_patch_url: str) -> str:
        response = requests.get(pr_patch_url)
        if response.status_code != 200:
            return f"Error fetching PR patch: {response.status_code}"
        return response.text

class RelatedPRsInput(BaseModel):
    """Input schema for FindRelatedPRsTool."""
    repo_name: str = Field(..., description="Full repository name (owner/repo)")
    file_paths: List[str] = Field(..., description="List of file paths to find related PRs for")

class FindRelatedPRsTool(BaseTool):
    name: str = "Find Related Pull Requests"
    description: str = "Searches for and analyzes related pull requests that modified similar files"
    args_schema: Type[BaseModel] = RelatedPRsInput

    def _run(self, repo_name: str, file_paths: List[str]) -> str:
        token = os.getenv('GITHUB_TOKEN')
        g = Github(token)
        repo = g.get_repo(repo_name)
        related_prs = []

        for pr in repo.get_pulls(state='closed'):
            files = pr.get_files()
            if any(f.filename in file_paths for f in files):
                related_prs.append({
                    'number': pr.number,
                    'title': pr.title,
                    'url': pr.html_url,
                    'body': pr.body
                })

        return related_prs[:5]  # Return top 5 related PRs

class RelatedFilesInput(BaseModel):
    """Input schema for FindRelatedFilesTool."""
    repo_name: str = Field(..., description="Full repository name (owner/repo)")
    file_paths: List[str] = Field(..., description="List of modified file paths")

class FindRelatedFilesTool(BaseTool):
    name: str = "Find Related Files"
    description: str = "Identifies files that are functionally related to the modified files"
    args_schema: Type[BaseModel] = RelatedFilesInput

    def _run(self, repo_name: str, file_paths: List[str]) -> str:
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ValueError("GitHub token not provided in environment or parameters")
        g = Github(token)
        repo = g.get_repo(repo_name)
        related_files = []

        for file_path in file_paths:
            # Get the file content to analyze imports and dependencies
            try:
                content = repo.get_contents(file_path)
                # Add logic here to parse file content and find related files
                # This could include:
                # - Files in the same directory
                # - Files imported/referenced
                # - Parent classes
                # - Interface implementations
                related_files.extend(self._analyze_file_relations(content.decoded_content))
            except Exception as e:
                continue

        return list(set(related_files))  # Return unique related files

    def _analyze_file_relations(self, content: str) -> List[str]:
        # Add your logic to analyze file content and find relations
        # This is a placeholder that should be implemented based on your needs
        return []

class CodeReviewInput(BaseModel):
    """Input schema for GenerateReviewTool."""
    analysis_results: str = Field(..., description="Results from code analysis")
    related_prs: str = Field(..., description="Information about related PRs")
    related_files: str = Field(..., description="Information about related files")

class GenerateReviewTool(BaseTool):
    name: str = "Generate Code Review"
    description: str = "Generates a comprehensive code review comment based on all analyses"
    args_schema: Type[BaseModel] = CodeReviewInput

    def _run(self, analysis_results: str, related_prs: str, related_files: str) -> str:
        # Combine all inputs into a well-structured markdown review
        review = f"""
# Code Review Summary

## Code Analysis
{analysis_results}

## Historical Context
{related_prs}

## Related Files Impact
{related_files}

## Recommendations
- [Add prioritized recommendations based on the analysis]
"""
        return review