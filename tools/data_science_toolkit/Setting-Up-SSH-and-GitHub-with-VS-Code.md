# How to Set Up SSH Keys and Connect VS Code to GitHub

This guide walks through setting up SSH keys on your local machine, adding them to your GitHub account, and configuring Visual Studio Code (VS Code) to connect to GitHub using SSH. We will also discuss some common issues you might encounter, especially on Windows.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Step 1: Generate SSH Keys](#step-1-generate-ssh-keys)
   - [Windows Specific Issues](#windows-specific-issues)
3. [Step 2: Add the SSH Key to the SSH Agent](#step-2-add-the-ssh-key-to-the-ssh-agent)
   - [Common SSH Agent Issues on Windows](#common-ssh-agent-issues-on-windows)
4. [Step 3: Add SSH Key to GitHub](#step-3-add-ssh-key-to-github)
5. [Step 4: Configure VS Code to Work with GitHub](#step-4-configure-vs-code-to-work-with-github)
6. [Step 5: Test SSH Connection to GitHub](#step-5-test-ssh-connection-to-github)
7. [Step 6: Working with GitHub in VS Code](#step-6-working-with-github-in-vs-code)
8. [Conclusion](#conclusion)

---

## Prerequisites

- **Git**: Make sure Git is installed on your system. You can check this by running `git --version` in your terminal. If not installed, download it from [here](https://git-scm.com/downloads).
- **GitHub Account**: You need a GitHub account. Sign up [here](https://github.com/) if you don't have one.
- **Visual Studio Code**: Ensure you have VS Code installed on your machine. Download it [here](https://code.visualstudio.com/).

---

## Step 1: Generate SSH Keys

We need to create an SSH key pair that will be used to authenticate your local machine with GitHub.

### Instructions

1. **Open a terminal** (Git Bash on Windows, Terminal on macOS or Linux, or PowerShell).
2. Run the following command to generate a new SSH key:

   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```
   Replace "your_email@example.com" with your actual email address associated with your GitHub account.

3. You will be prompted to choose a location to save the SSH key. Press **Enter** to accept the default location
4. **Passphrase (optional but highly recommended)**: You can add a passphrase for extra security, or press **Enter** to skip.

**Windows Specific Issues**
If you're on Windows, sometimes specifying paths in commands might not work directly. If needed, use the full path to the SSH key files (e.g., `C:\Users\your_user\.ssh\id_ed25519`).

## Step 2: Add the SSH Key to the SSH Agent

Next, we need to add the SSH private key to the SSH agent, which will manage your keys.

**Instructions**
**1. Start the SSH agent:**

- On **macOS/Linux**:
```bash
eval "$(ssh-agent -s)"
```
- On **Windows**, run the following in **PowerShell (Administrator)**:
```bash
Start-Service ssh-agent
```
2. **Add your private key to the agent**:
- On macOS/Linux:
```bash
ssh-add ~/.ssh/id_ed25519
```
- On Windows, run the following in PowerShell (Administrator):
```bash
ssh-add C:\Users\your_user\.ssh\id_ed25519
```
**Common SSH Agent Issues on Windows**
- If you encounter an error like `unable to start ssh-agent service, error: 1058`, it means the service is disabled. Run the following in **PowerShell (Administrator)**:
```bash
Set-Service -Name ssh-agent -StartupType Manual
Start-Service ssh-agent
```
- If the `ssh-add` command gives an error like "No such file or directory," ensure you are specifying the correct path to the private key file.

## Step 3: Add SSH Key to GitHub
Now that the SSH key is generated and added to the agent, we need to add the public key to GitHub.

**Instructions**
1. Copy the SSH public key to your clipboard:
- On macOS/Linux:
```bash
cat ~/.ssh/id_ed25519.pub
```
- On Windows, run the following in PowerShell (Administrator):
```bash
cat C:\Users\your_user\.ssh\id_ed25519.pub 
```
2. Go to GitHub and log in to your account.

3. Navigate to **Settings > SSH and GPG keys > New SSH key**.

4. In the **Title** field, add a descriptive name (e.g., "VS Code SSH Key").

5. Paste the public key into the **Key** field.

6. Click **Add SSH key**.

## Step 4: Configure VS Code to Work with GitHub
**Clone a Repository Using SSH**
1. Open VS Code.
2. Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on macOS) to open the Command Palette.
3. Search for **Git: Clone** and select it.
4. Paste your repository's SSH URL, which can be found on GitHub:
- Navigate to your repository, click the green **Code** button, and select **SSH**.
- The URL will look like this: `git@github.com:username/repository-name.git`.
5. Select a folder to clone the repository locally.
6. VS Code will clone the repository and prompt you to open the folder.

## Step 5: Test SSH Connection to GitHub
To confirm that your SSH setup is working, run the following command in the terminal:
```bash
ssh -T git@github.com
```

If everything is set up correctly, you'll see a message like this:
```bash
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

## Step 6: Working with GitHub in VS Code
**Commit and Push Changes**
1. Make changes to your project files.
2. Open the **Source Control** panel in VS Code (or press `Ctrl + Shift + G`).
3. Write a commit message in the message box.
4. Click the checkmark icon to commit your changes.
5. To push your changes to GitHub, click the ... in the Source Control panel and select **Push**.

**Pull Changes**
To pull the latest changes from GitHub:

1. In the **Source Control** panel, click the ... menu.
2. Select **Pull**.

**Conclusion**
You have successfully configured SSH keys on your local machine, added them to GitHub, and connected VS Code to GitHub using SSH. You're now ready to clone, commit, push, and pull code securely and efficiently. If you encounter any issues, refer back to the steps and troubleshooting tips in this guide.
