from openai import OpenAI


class CommitAnalyzer:

    def __init__(self, api_key: str, prompt: str):
        self.__prompt = prompt
        self.__client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=api_key,
        )

        self.__messages = [
            {
                "role": "system",
                "content": self.__prompt
            }]

    def generate_report(self, git_commits: str) -> str:
        # noinspection PyTypeChecker
        completion = self.__client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=self.__messages + [
                {
                    "role": "user",
                    "content": f"Can you analyze this carefully?\n\n{git_commits}"
                }
            ]
        )
        return completion.choices[0].message.content
