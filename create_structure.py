import os
from pathlib import Path

def create_project_structure():
    # Base project directory
    base_dir = Path("tradeguard-ai-backend")

    # List of all the files to be created
    # pathlib will automatically handle the Windows backslashes (\)
    files_to_create = [
        base_dir / "app" / "main.py",
        base_dir / "app" / "database.py",
        base_dir / "app" / "models.py",
        base_dir / "app" / "schemas.py",
        base_dir / "app" / "auth.py",
        base_dir / "app" / "analytics.py",
        base_dir / "app" / "routers" / "auth_routes.py",
        base_dir / "app" / "routers" / "trade_routes.py",
        base_dir / "app" / "routers" / "risk_routes.py",
        base_dir / "requirements.txt",
        base_dir / "sample_trades.csv"
    ]

    print(f"Creating project structure for '{base_dir}'...\n")

    for file_path in files_to_create:
        # Create parent directories (like app/ or app/routers/) if they don't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create the empty file
        file_path.touch(exist_ok=True)
        
        print(f"Created: {file_path}")

    print("\n✅ Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()