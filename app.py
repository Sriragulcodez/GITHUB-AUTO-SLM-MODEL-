import streamlit as st
import subprocess
import os

# ==============================
# ⚙️ CONFIG
# ==============================
st.set_page_config(page_title="Git-Auto Pro", layout="centered")

st.title("🚀 Git-Auto Pro (SLM Edition)")
st.write("Mini GitHub Desktop + AI Git Assistant")

# ==============================
# 🧠 AI INTENT DETECTION
# ==============================
def detect_intent(command):
    command = command.lower()

    if "clone" in command:
        return "clone"
    elif "push" in command:
        return "push"
    elif "status" in command:
        return "status"
    else:
        return "unknown"


# ==============================
# 📊 GIT STATUS
# ==============================
def show_git_summary(folder_path):
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=folder_path,
            capture_output=True,
            text=True
        )

        st.subheader("📊 Git Status")
        st.code(result.stdout if result.stdout else "Clean working tree")

    except Exception as e:
        st.error(str(e))


# ==============================
# 📤 PUSH PROJECT
# ==============================
def push_project(repo_url, folder_path):
    try:
        if not os.path.exists(folder_path):
            st.error("❌ Folder does not exist")
            return

        st.write("📦 Initializing Git...")

        cmds = [
            ["git", "init"],
            ["git", "add", "."],
            ["git", "commit", "-m", "Auto commit from Git-Auto Pro"],
            ["git", "branch", "-M", "main"]
        ]

        for cmd in cmds:
            res = subprocess.run(cmd, cwd=folder_path, capture_output=True, text=True)
            st.text(res.stdout)
            st.text(res.stderr)

        # Safe remote handling
        subprocess.run(["git", "remote", "remove", "origin"], cwd=folder_path, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=folder_path)

        st.write("🚀 Pushing to GitHub...")

        push = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=folder_path,
            capture_output=True,
            text=True
        )

        st.text(push.stdout)
        st.text(push.stderr)

        if push.returncode == 0:
            st.success("🎉 Push Successful!")
        else:
            st.error("❌ Push Failed")

    except Exception as e:
        st.error(str(e))


# ==============================
# 📥 CLONE REPO (PRO FIXED)
# ==============================
def clone_repo(repo_url, clone_path):
    try:
        if not repo_url:
            st.error("❌ Repo URL required")
            return None

        if not clone_path:
            st.error("❌ Please enter clone path")
            return None

        repo_name = repo_url.split("/")[-1].replace(".git", "")
        target_path = os.path.join(clone_path, repo_name)

        # Auto-create folder if not exists
        os.makedirs(clone_path, exist_ok=True)

        # Prevent overwrite issue
        if os.path.exists(target_path):
            st.warning("⚠️ Folder already exists, using existing directory")

        st.write(f"📥 Cloning into: {target_path}")

        result = subprocess.run(
            ["git", "clone", repo_url, target_path],
            capture_output=True,
            text=True
        )

        st.text(result.stdout)
        st.text(result.stderr)

        if result.returncode == 0:
            st.success("✅ Clone Successful!")
            return target_path
        else:
            st.error("❌ Clone Failed")
            return None

    except Exception as e:
        st.error(str(e))
        return None


# ==============================
# 🎯 UI
# ==============================
mode = st.radio("Choose Mode", ["Manual", "AI Command"])

repo_url = st.text_input("🔗 GitHub Repo URL")

folder_path = st.text_input("📁 Project Folder Path (for push)")
clone_path = st.text_input("📂 Clone Location Path")

user_command = ""
if mode == "AI Command":
    user_command = st.text_input("💬 Enter command (e.g. clone this repo / push project / status)")

action = ""
if mode == "Manual":
    action = st.selectbox("⚡ Choose Action", ["Push Project", "Clone Repo", "Git Status"])


# ==============================
# ▶️ RUN ENGINE
# ==============================
if st.button("Run"):
    st.write("### 🔧 Output")

    try:
        if mode == "AI Command":

            intent = detect_intent(user_command)

            if intent == "clone":
                path = clone_repo(repo_url, clone_path)
                if path:
                    st.write(f"📂 Cloned at: {path}")

            elif intent == "push":
                show_git_summary(folder_path)
                push_project(repo_url, folder_path)

            elif intent == "status":
                show_git_summary(folder_path)

            else:
                st.warning("❌ Could not understand command")

        else:

            if action == "Clone Repo":
                path = clone_repo(repo_url, clone_path)
                if path:
                    st.write(f"📂 Cloned at: {path}")

            elif action == "Push Project":
                show_git_summary(folder_path)
                push_project(repo_url, folder_path)

            elif action == "Git Status":
                show_git_summary(folder_path)

    except Exception as e:
        st.error(str(e))