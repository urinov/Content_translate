import os
import subprocess
import sys

def run(command):
    """Run a shell command."""
    subprocess.check_call(command, shell=True)

def create_virtualenv():
    """Create a virtual environment."""
    if not os.path.exists("venv"):
        run("python3 -m venv venv")
        print("Virtual environment created.")
    else:
        print("Virtual environment already exists.")

def install_requirements():
    """Install required libraries."""
    run("pip install --upgrade pip")
    run("pip install python-telegram-bot python-dotenv")

def setup_bot():
    """Setup bot environment."""
    print("Setting up the bot environment...\n")
    
    # Create virtual environment
    create_virtualenv()
    
    # Activate virtual environment
    if sys.platform == "win32":
        activate_this = "./venv/Scripts/activate_this.py"
    else:
        activate_this = "./venv/bin/activate_this.py"
    
    # Install required packages
    install_requirements()
    
    # Setup .env file
    if not os.path.exists(".env"):
        print(".env file not found, creating one...")
        with open(".env", "w") as f:
            f.write("BOT_TOKEN=your_bot_token_here\n")
            f.write("CHANNEL_USERNAME=your_channel_username_here\n")
        print(".env file created.")
    else:
        print(".env file already exists.")

if __name__ == "__main__":
    setup_bot()
    print("Bot setup completed!")
