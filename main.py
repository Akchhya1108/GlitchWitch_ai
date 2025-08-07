from dotenv import load_dotenv
import os

load_dotenv()
print("API KEY (preview):", os.getenv("OPENAI_API_KEY")[:10])

from core.run_luna import run_luna

if __name__ == "__main__":
    run_luna()

ascii_logo = r"""
   ⛧ LUNA the GLITCHWITCH ⛧
        ／＞　 フ
       | 　_　_| 
     ／` ミ＿xノ 
    /　　　　 |
   /　 ヽ　　 ﾉ
 │　　|　|　|
／￣|　　 |　|　|
(￣ヽ＿_ヽ_)__)
＼二)
"""
print(ascii_logo)