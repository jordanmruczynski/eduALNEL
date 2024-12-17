from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain

def get_quiz_data(text, openai_api_key, difficulty, num_questions, language):
    template = f"""
    You are a helpful assistant programmed to generate {num_questions} questions based on any text provided. The questions and answers should match the difficulty on {difficulty} level and be in {language} language.
    Each of these questions will be accompanied by 3 possible answers: one correct answer and two incorrect ones. 

    For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 

    Your output should be shaped as follows:

    1. An outer list that contains {num_questions} inner lists.
    2. Each inner list represents a set of question and answers, and contains exactly 4 strings in this order:
    - The generated question.
    - The correct answer.
    - The first incorrect answer.
    - The second incorrect answer.

    Your output should mirror this structure:
    [
        ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2"],
        ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2"],
        ...
    ]

    It is crucial that you adhere to this format as it's optimized for further Python processing.

    """
    try:
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt, human_message_prompt
        ])
        chain = LLMChain(
            llm=ChatOpenAI(openai_api_key=openai_api_key),
            prompt=chat_prompt,
        )
        return chain.run(text)
    except Exception as e:
        raise RuntimeError(f"Error during quiz generation: {str(e)}")

def string_to_list(data_str):
    """Converts a string representation of a Python list to an actual list."""
    try:
        return eval(data_str)
    except Exception as e:
        raise ValueError(f"Error parsing quiz data string: {str(e)}")

def get_randomized_options(answers):
    """Randomizes the order of the answers and returns them along with the correct one."""
    import random
    correct_answer = answers[0]
    all_options = answers[:]
    random.shuffle(all_options)
    return all_options, correct_answer