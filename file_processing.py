from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

class FileProcessingClass:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")


    def process_file(self, file_path: str, prompt: str) -> None:
        with open(file_path, 'r') as file:
            file_content = file.read()

        prompt_with_file_content = f"system: You are a programmer. You respond only with working code. You do not speak natural languages, but only programming languages so you don't explain\n\nTask:{prompt}\n\nFileContent:{file_content}\n\nUpdatedFileContent:"
        result = self.llm.invoke(prompt_with_file_content)

        with open(file_path, 'w') as file:
            file.write(result.content)

