import streamlit as st
import time
import requests

base_url = st.secrets["base_url"]
bearer_token = st.secrets["bearer_token"]

st.set_page_config(
    page_title="CrewAI Pull Request Review Agents",
    page_icon="🦾",
    layout="wide"
)

# Initialize session state for storing the kickoff_id and polling status
def reset_session_state():
    st.session_state.kickoff_id = None
    st.session_state.polling = False
    st.session_state.result = None
    st.session_state.button_disabled = False

if 'kickoff_id' not in st.session_state:
    st.session_state.kickoff_id = None
if 'polling' not in st.session_state:
    st.session_state.polling = False
if 'result' not in st.session_state:
    st.session_state.result = None
if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False

st.logo("https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg", link="https://www.crewai.com/", size="large")

st.sidebar.title("CrewAI Pull Request Review Agents")

st.sidebar.markdown("""
**Welcome to automated Code Review with CrewAI Multi-Agent Crew!**  
Here, you’ll discover how our specialized agents can review **any** GitHub pull request, streamlining your development workflow.

Simply enter the URL of the pull request in the form below, and let CrewAI do the rest!

If you’d like to explore the underlying code, feel free to check out the [source for this Crew](https://github.com/crewAIInc/demo-pull-request-review).

Here are some examples of how this Crew reviews our Pull Requests:
* [crewaiinc/crewai: PR #1947](https://github.com/crewAIInc/crewAI/pull/1947)
* [crewaiinc/crewai: PR #1923](https://github.com/crewAIInc/crewAI/pull/1923)
* [crewaiinc/crewai: PR #1773](https://github.com/crewAIInc/crewAI/pull/1773)

**Interested in having this Crew automatically post comments on your GitHub pull requests?**

Simply [open a CrewAI platform account](https://app.crewai.com/), fork the repository, make any necessary changes, and deploy the Crew to your account. It’s quick, easy, and will supercharge your pull request reviews with faster, smarter feedback!
""")

st.sidebar.link_button("Open a CrewAI platform account", "https://app.crewai.com/", type="primary")

reset_button = st.sidebar.button(
    "Reset this page",
    on_click=reset_session_state
)

def kickoff_callback():
    if not st.session_state.pr_patch_url:
        st.warning("Please enter a PR Patch URL")
        return

    try:
        # Extract repository name from PR patch URL
        pr_patch_url_parts = st.session_state.pr_patch_url.split('/')
        repo_name = f"{pr_patch_url_parts[3]}/{pr_patch_url_parts[4]}".lower()

        # Build the request body
        request_body = {
            "inputs": {
                "repo_name": repo_name,
                "pr_patch_url": st.session_state.pr_patch_url + ".patch",
                "files_changed": ""
            },
            "taskWebhookUrl": "",
            "stepWebhookUrl": "",
            "crewWebhookUrl": "",
            "trainingFilename": "",
            "generateArtifact": False
        }

        # Make the POST request
        response = requests.post(
            f'{base_url}/kickoff',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {bearer_token}',
            },
            json=request_body
        )

        if response.status_code != 200:
            st.error(f"Error: {response.text}")
            return

        data = response.json()
        st.session_state.kickoff_id = data.get('kickoff_id')
        # st.session_state.kickoff_id = "4f2b708b-aae6-4a8e-8649-276b54f56f85"
        st.session_state.polling = True
        st.session_state.result = None
        st.session_state.button_disabled = True

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Input for PR URL
with st.form(key='pr_form'):
    pr_patch_url = st.text_input(
        "PR Patch URL",
        placeholder="e.g. https://github.com/user/my-repo/pull/123",
        key='pr_patch_url'
    )

    submit_button = st.form_submit_button(
        "Review Code", 
        type="primary", 
        disabled=st.session_state.button_disabled, 
        on_click=kickoff_callback
    )


# Create a placeholder for the result
result_placeholder = st.empty()

# If we have a result, display it
if st.session_state.result:
    result_placeholder.markdown(st.session_state.result)
    st.session_state.button_disabled = False
elif st.session_state.polling:
    with st.spinner('Wait for it... (it can take a couple of minutes depending on the size of the PR)'):
        while st.session_state.polling:
            try:
                response = requests.get(
                    f'{base_url}/status/{st.session_state.kickoff_id}',
                    headers={'Authorization': f'Bearer {bearer_token}'}
                )

                if response.status_code != 200:
                    st.error(f"Error checking status: {response.text}")
                    st.session_state.polling = False
                    st.session_state.button_disabled = False
                    break

                data = response.json()

                if data.get('state') == 'SUCCESS':
                    st.session_state.polling = False
                    st.session_state.result = data.get('result')
                    st.session_state.button_disabled = False

                    st.markdown(data.get('result'))
                    break
                
                time.sleep(30)  # Poll every 30 seconds
                
            except Exception as e:
                st.error(f"Error checking status: {str(e)}")
                st.session_state.polling = False
                st.session_state.button_disabled = False
                break
