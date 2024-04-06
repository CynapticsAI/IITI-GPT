import os

query = "Which clubs are there at IIT Indore?"

os.system("rm output1.wav | true")

os.system("""curl --location 'https://a83f-103-159-214-187.ngrok-free.app/query' \
          --header 'Content-Type:application/json' \
          --data '{"base_prompt":"{"""+query +"""}", "history": []}' -o output1.mp3""")