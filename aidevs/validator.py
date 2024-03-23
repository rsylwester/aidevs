import openai_proxy


def validate_relevation_of_answer(question, answer):
    result = openai_proxy.ask_gpt(system=f"""Sprawdzasz czy podana odpowiedź jest zgodna z tematem pytania. Jeżeli jest zgodna odpowiadasz 'YES', jeżeli nie jest zgodna odpowiadasz 'NO'.
    Pytanie brzmi: '{question}'""", question=answer)

    print(f"validation result: {result}")

    return result