import os

# Assume OPENAI_API_KEY is currently set (e.g., in your shell or .env file)
print(f"Before removal: {os.environ.get('OPENAI_API_KEY')}")

# To "remove" it for the current process:
if "OPENAI_API_KEY" in os.environ:
    del os.environ["OPENAI_API_KEY"]
    print("OPENAI_API_KEY removed for this process.")
else:
    print("OPENAI_API_KEY was not set in this process's environment.")

print(f"After removal: {os.environ.get('OPENAI_API_KEY')}")