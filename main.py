from core.run_luna import run_luna

if __name__ == "__main__":
    run_luna()

# TEMP TEST:
from core.mood import get_recent_moods
print("\nRecent mood logs:")
for log in get_recent_moods():
    print(log)
