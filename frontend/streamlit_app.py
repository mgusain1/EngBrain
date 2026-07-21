import streamlit as st
import requests
import uuid

API_BASE = "https://engbrain-api.onrender.com"

st.set_page_config(
    page_title="EngBrain",
    layout="wide"
)

st.title("EngBrain")
st.write("AI engineering memory and runbook generator for codebases.")
st.info(
    "Beta note: use public GitHub repositories only. "
    "Repo URLs, questions, answers, and source file references may be logged for product feedback."
)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.caption("Session: " + st.session_state.session_id)

st.header("1. Ingest Repository")

repo_path = st.text_input(
    "Local repo path or public GitHub URL",
    value=r"https://github.com/octocat/Hello-World"
)

if st.button("Ingest Repo"):
    try:
        response = requests.post(
            f"{API_BASE}/repos/ingest",
            json = {"repo_path":repo_path, "session_id": st.session_state.session_id}
        )
        if response.status_code == 200:
            st.success("Repo Successfully Ingested")
            st.json(response.json())
        else:
            st.error("Error in Ingesting")
            st.text(response.text)
    except Exception as e:
        st.error(f"could not connect to backend: {e}")
    
st.header("2. Select Repository")

repos = []
try:
    response = requests.get(f"{API_BASE}/repos")
    if response.status_code == 200:
        repos = response.json()
    else:
        st.warning("Could not reach Repo")
        
except Exception as e:
    st.warning(f"Backend is not availble because :{e}")

selected_repo = None
if repos:
    repo_option = {}
    for repo in repos:
        label = str(repo["repo_id"]) + " - " + repo["repo_name"]
        repo_option[label] = repo["repo_id"]
        
    selected_label = st.selectbox(
        "Choose Repo",
        list(repo_option.keys())
    )
    selected_repo = repo_option[selected_label]
else:
    st.info("No repos found. Ingest a repo first")
    
st.header("3. Ask a Question")
question = st.text_input(
    "Question",
    value="How does Ingestion Work?"
)

top_k = st.slider(
    "Top K sources",
    min_value=1,
    max_value=10,
    value=5
)

if st.button("Ask Engbrain"):
    if selected_repo is None:
        st.error("Please Select a Repo first")
    else:
        try:
            response = requests.post(
                API_BASE+"/ask",
                json = {
                    "repo_id":selected_repo,
                    "question": question,
                    "top_k": top_k,
                    "session_id": st.session_state.session_id
                }
            )
            if response.status_code == 200:
                data = response.json()
                st.subheader("Answer")
                st.write(data.get("answer",""))
                st.subheader("Sources")
                sources = data.get("sources",[])
                if sources and isinstance(sources[0], list):
                    sources = sources[0]
                if not sources:
                    st.info("No sources returned.")
                else:
                    source_number =1 
                    for source in sources:
                        file_path = source.get("file_path", "unknown file")
                        start_line = source.get("start_line", "")
                        end_line = source.get("end_line", "")

                        title = "Source" + str(source_number) + ": "+ file_path + " lines " + str(start_line) + "-" + str(end_line)
                        source_number+=1
                        with st.expander(title):
                            preview = source.get("preview")

                            if preview is None:
                                preview = source.get("text", "")

                            st.code(preview)
            else:
                st.error("Ask request failed.")
                st.text(response.text)
        except Exception as e:
            st.error("Could not connect to backend.")
            st.text(str(e))
            
st.header("4. Generate Runbook")
task = st.text_input(
    "Runbook Task",
    value="Debug failed ingestion"
)

if st.button("Generate Runbook"):
    if selected_repo is None:
        st.warning("Please select a Repo first")
    else:
        try:
            response = requests.post(
                API_BASE+"/runbook",
                json = {
                     "repo_id": selected_repo,
                      "task": task,
                      "top_k": top_k,
                      "session_id": st.session_state.session_id
                }
            )
            if response.status_code == 200:
                data = response.json()

                st.subheader("Runbook")
                st.write(data.get("runbook", ""))

                st.subheader("Sources")

                sources = data.get("sources", [])
                if sources and isinstance(sources[0], list):
                    sources = sources[0]
                if not sources:
                    st.info("No sources returned.")
                else:
                    source_number = 1
                    for source in sources:
                        file_path = source.get("file_path", "unknown file")
                        start_line = source.get("start_line", "")
                        end_line = source.get("end_line", "")
                        title = "Source" + str(source_number) + ": "+ file_path + " lines " + str(start_line) + "-" + str(end_line)
                        source_number+=1

                        with st.expander(title):
                            preview = source.get("preview")

                            if preview is None:
                                preview = source.get("text", "")

                            st.code(preview)

            else:
                st.error("Runbook request failed.")
                st.text(response.text)

        except Exception as e:
            st.error("Could not connect to backend.")
            st.text(str(e))