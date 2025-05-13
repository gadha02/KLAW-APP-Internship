import google.generativeai as genai

api_key = 'AIzaSyBAe2J74E9lUSSkNhC2k3em3cv4MsWd534'
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = input("Enter your question for Gemini: ")
response = model.generate_content(prompt)

print("Gemini Response:\n")
print(response.text)
