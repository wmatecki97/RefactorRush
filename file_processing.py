from langchain_openai import ChatOpenAI

class FileProcessingClass:
    def __init__(self):
        self.llm =  ChatOpenAI(
    base_url="http://localhost:1234/v1",
    temperature=0,
    api_key="not-needed"
)

    def process_file(self, file_path: str, prompt: str) -> None:
        with open(file_path, 'r') as file:
            file_content = file.read()

        prompt_with_file_content = f"system: You are a programmer. You respond only with working code. You do not speak natural languages, but only programming languages so you don't explain\n\nTask:{prompt}\n\nFileContent:{file_content}\n\nUpdatedFileContent:"
        result = self.llm.invoke(prompt_with_file_content)

        with open(file_path, 'w') as file:
            file.write(result.content.replace('```python\n', '').replace('```', ''))

    def test(self, question):
        result = self.llm.invoke(question)
        print(result.content)

