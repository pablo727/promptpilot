import openai


class OpenAIService:
    @staticmethod
    def run_prompt(prompt_text, input_vars):
        full_prompt = prompt_text.format(**input_vars)
        response = openai.ChatCompletion.create(
            model="gpt-4", messages=[{"role": "user", "content": full_prompt}]
        )
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        return {"result": content, "tokens_used": tokens}
