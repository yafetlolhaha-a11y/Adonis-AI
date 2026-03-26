from google import genai

# Configure client with your API key
client = genai.Client(api_key="AIzaSyDn0tKuUFcb3ZDDot3wjarlvWia-8UVDrk")

# Generate content
response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Explain how AI works in a few words"
)

# Print the result
print(response.text)