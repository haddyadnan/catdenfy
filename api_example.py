import requests
import base64

with open("static/images/index.jpeg", "rb") as img_file:
    img_str = base64.b64encode(img_file.read()).decode()

response = requests.post(
    "https://haddy-catdenfy.hf.space/run/predict",
    json={
        "data": [
            "data:image/png;base64,{}".format(img_str),
        ]
    },
).json()

results = response["data"][0]
print(results.get("label").replace("_", " "))
probs = results.get("confidences")
probs_dict = {list(p.values())[0].replace("_", " "): list(p.values())[1] for p in probs}
print(probs_dict)
