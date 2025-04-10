# scripts/migrate.py
import subprocess

def migrate():
    subprocess.run(["alembic", "revision", "--autogenerate", "-m", "Auto migration"])
    subprocess.run(["alembic", "upgrade", "head"])

if __name__ == "__main__":
    migrate()
