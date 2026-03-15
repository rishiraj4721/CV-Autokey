
import sys

from dotenv import load_dotenv
from cv_autokey import CVAutoKey


def main():
    load_dotenv()
    config_path = sys.argv[1]
    url = sys.argv[2]
    
    cv_auto_key = CVAutoKey(config_path)
    cv_auto_key.run(url)

if __name__ == "__main__":
    main()