import requests

from llm_word_parser.llm.LLM import LLM


class Llama(LLM):
    def __init__(self) -> None:
        self.api_url = "http://localhost:11434/api/generate"
        self.model = "llama3"  # Change this to "llama3 8B" if needed

    def answer(self, llm_prompt: str) -> str:
        data = {
            "model": self.model,
            "prompt": llm_prompt,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()  # Raise an exception if status code is not 200
            return response.json()["response"]
        except requests.RequestException as e:
            return f"Error: {e}"


# Example usage
if __name__ == "__main__":
    llama = Llama()
    prompt = "Why is the sky blue?"
    answer = llama.answer(prompt)
    print(f"Answer: {answer}")
