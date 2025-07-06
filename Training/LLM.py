import google.generativeai as genai


def LLM_classification(msg):
    genai.configure(api_key="AIzaSyC5xKSQWHsdc3iAwOCgSIAT8XHp9Ie-28w")

    model = genai.GenerativeModel("gemini-1.5-flash")


    prompt = f"Given the Log message as follows: {msg}. classify it in these two categories only :[Workflow Error,Deprecation Warning], NO PREMEBLE"

    response = model.generate_content(prompt)

    return response.text
