import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    print("teste")
    print(os.getenv("OPENAI_API_KEY"))
    print(os.environ["OPENAI_API_KEY"])