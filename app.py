import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Git-Auto", layout="centered")

st.title("🚀 Git-Auto")
st.write("AI-powered Push • Clone • Run projects")

# ==============================
# 🧠 Intent Detection
# ==============================
def detect_intent(command):
    command = command.lower()

    if "clone" in command and "run" in command:
        return "clone_run"
    elif "clone" in command:
        return "clone"
    elif "push" in command:
        return "push"
    else:
        return "unknown"

# ==============================
# ▶️ Run Project
# ==============================
def run_project(project_path):
    try:
        if not os.path.exists(project_path):
            st.error("❌ Project folder not found")
            return

        files = os.listdir(project_path)

        if "package.json" in files:
            st.write("📦 Node/React project detected")
            subprocess.run("npm install", cwd=project_path, shell=True)
            subprocess.Popen("npm start", cwd=project_path, shell=True)

        elif "requirements.txt" in files:
            st.write("🐍 Python project detected")
            subprocess.run("pip install -r requirements.txt", cwd=project_path, shell=True)
            subprocess.Popen("python app.py", cwd=project_path, shell=True)

        else:
            st.warning("⚠️ Unknown project type")

    except Exception as e:
        st.error(str(e))

# ==============================
# 📤 Push Project
# ==============================
def push_project(repo_url, folder_path):
    try:
        if not os.path.exists(folder_path):
            st.error("❌ Invalid folder path")
            return

        commands = [
            ["git", "init"],
            ["git", "add", "."],
            ["git", "commit", "-m", "Auto commit from Git-Auto"],
            ["git", "branch", "-M", "main"]
        ]

        for cmd in commands:
            st.text(f"$ {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=folder_path, capture_output=True, text=True)
            st.text(result.stdout)
            st.text(result.stderr)

        # Remove origin if exists (ignore error)
        subprocess.run(["git", "remote", "remove", "origin"], cwd=folder_path, capture_output=True)

        subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=folder_path)

        result = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=folder_path,
            capture_output=True,
            text=True
        )

        st.text(result.stdout)
        st.text(result.stderr)

        if result.returncode == 0:
            st.success("🚀 Project pushed successfully!")

    except Exception as e:
        st.error(str(e))

# ==============================
# 📥 Clone Repo
# ==============================
def clone_repo(repo_url):
    result = subprocess.run(
        ["git", "clone", repo_url],
        capture_output=True,
        text=True
    )

    st.text(result.stdout)
    st.text(result.stderr)

    if result.returncode == 0:
        folder_name = repo_url.split("/")[-1].replace(".git", "")
        st.success(f"✅ Cloned: {folder_name}")
        return folder_name
    else:
        st.error("❌ Clone failed")
        return None

# ==============================
# 📊 Git Summary
# ==============================
def show_git_summary(folder_path):
    try:
        if not os.path.exists(folder_path):
            return

        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=folder_path,
            capture_output=True,
            text=True
        )

        st.write("📊 Changes Summary:")
        st.text(result.stdout)

    except:
        pass

# ==============================
# 🎯 UI
# ==============================

mode = st.radio("Choose Mode", ["Manual", "AI Command"])

repo_url = st.text_input("Enter Repository URL")
folder_path = st.text_input("Project Folder Path (for push)")

user_command = ""
if mode == "AI Command":
    user_command = st.text_input("Enter command (e.g., 'clone and run this repo')")

action = ""
if mode == "Manual":
    action = st.selectbox("Choose Action", ["Push Project", "Clone Repo"])

# ==============================
# ▶️ RUN
# ==============================
if st.button("Run"):
    st.write("### 🔧 Output:")

    try:
        # AI MODE
        if mode == "AI Command":
            intent = detect_intent(user_command)

            if intent == "clone_run":
                folder = clone_repo(repo_url)
                if folder:
                    run_project(folder)

            elif intent == "clone":
                clone_repo(repo_url)

            elif intent == "push":
                show_git_summary(folder_path)
                push_project(repo_url, folder_path)

            else:
                st.warning("❌ Could not understand command")

        # MANUAL MODE
        else:
            if action == "Clone Repo":
                folder = clone_repo(repo_url)
                if folder:
                    run_project(folder)

            elif action == "Push Project":
                show_git_summary(folder_path)
                push_project(repo_url, folder_path)

    except Exception as e:
        st.error(str(e))