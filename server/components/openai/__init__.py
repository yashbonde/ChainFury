import requests
from typing import Any, List, Union, Dict

from fury import Secret, model_registry, exponential_backoff


def openai_completion(
    openai_api_key: Secret,
    model: str,
    prompt: Union[str, List[Union[str, List[str]]]],
    max_tokens: int = 16,
    temperature: float = 1,
    top_p: float = 1,
    n: int = 1,
    logprobs: int = 0,
    echo: bool = False,
    stop: Union[str, List[str]] = "",
    presence_penalty: float = 0,
    frequency_penalty: float = 0,
    best_of: int = 1,
    logit_bias: dict = {},
    user: str = "",
    *,
    raw: bool = False,
) -> Dict[str, Any]:
    """
    Generate text completion using OpenAI's GPT-3 API.

    Args:
        model (str): ID of the model to use.
        prompt (Union[str, List[Union[str, List[str]]]]): The prompt(s) to generate completions for.
            Encoded as a string, array of strings, array of tokens, or array of token arrays.
        max_tokens (Optional[int]): The maximum number of tokens to generate in the completion. Defaults to 16.
        temperature (Optional[float]): What sampling temperature to use, between 0 and 2. Defaults to 1.
        top_p (Optional[float]): An alternative to sampling with temperature. Defaults to 1.
        n (Optional[int]): How many completions to generate for each prompt. Defaults to 1.
        logprobs (Optional[int]): Include the log probabilities on the logprobs most likely tokens.
            The maximum value for logprobs is 5. Defaults to None.
        echo (Optional[bool]): Echo back the prompt in addition to the completion. Defaults to False.
        stop (Optional[Union[str, List[str]]]): Up to 4 sequences where the API will stop generating further tokens.
            The returned text will not contain the stop sequence. Defaults to None.
        presence_penalty (Optional[float]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
            whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
            Defaults to 0.
        frequency_penalty (Optional[float]): Number between -2.0 and 2.0. Positive values penalize new tokens based on
            their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line
            verbatim. Defaults to 0.
        best_of (Optional[int]): Generates best_of completions server-side and returns the "best".
            Results cannot be streamed. Defaults to 1.
        logit_bias (Optional[dict]): Modify the likelihood of specified tokens appearing in the completion.
            Accepts a json object that maps tokens (specified by their token ID in the GPT tokenizer) to an associated
            bias value from -100 to 100. Defaults to None.
        user (Optional[str]): A unique identifier representing your end-user, which can help OpenAI to monitor and detect
            abuse. Defaults to None.

    Returns:
        Any: The completion(s) generated by the API.

    """

    def _fn():
        r = requests.post(
            "https://api.openai.com/v1/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}",
            },
            json={
                "model": model,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "n": n,
                "logprobs": logprobs,
                "echo": echo,
                "stop": stop,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty,
                "best_of": best_of,
                "logit_bias": logit_bias,
                "user": user,
            },
        )
        if r.status_code != 200:
            raise Exception(f"OpenAI API returned status code {r.status_code}: {r.text}")
        return r.json()

    return exponential_backoff(_fn)


model_registry.register(
    fn=openai_completion,
    collection_name="openai",
    id="openai-completion",
    description="Given a prompt, the model will return one or more predicted completions, and can also return the "
    "probabilities of alternative tokens at each position.",
)


def openai_chat(
    openai_api_key: Secret,
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 1.0,
    top_p: float = 1.0,
    n: int = 1,
    stop: Union[str, List[str]] = "",
    max_tokens: int = 1024,
    presence_penalty: float = 0.0,
    frequency_penalty: float = 0.0,
    logit_bias: dict = {},
    user: str = "",
    *,
    retry_count: int = 5,
    max_retry_delay: int = 5,
) -> Any:
    """
    Returns a JSON object containing the OpenAI's API chat response.

    Args:
        model: ID of the model to use. See the model endpoint compatibility table for details on which models work with the Chat API.
        messages: A list of messages describing the conversation so far, each item contains the folowing keys
            role: The role of the author of this message. One of system, user, or assistant.
            content: The contents of the message.
            name: Optional. The name of the author of this message. May contain a-z, A-Z, 0-9, and underscores, with a maximum length of 64 characters.
        temperature: Optional. What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both. Defaults to 1.
        top_p: Optional. An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered. We generally recommend altering this or temperature but not both. Defaults to 1.
        n: Optional. How many chat completion choices to generate for each input message. Defaults to 1.
        stop: Optional. Up to 4 sequences where the API will stop generating further tokens.
        max_tokens: Optional. The maximum number of tokens to generate in the chat completion. The total length of input tokens and generated tokens is limited by the model's context length. Defaults to infinity.
        presence_penalty: Optional. Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. See more information about frequency and presence penalties. Defaults to 0.
        frequency_penalty: Optional. Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim. See more information about frequency and presence penalties. Defaults to 0.
        logit_bias: Optional. Modify the likelihood of specified tokens appearing in the completion. Accepts a json object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant
        user: Optional. A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse. Defaults to None.

    Returns:
        Any: The completion(s) generated by the API.
    """

    def _fn():
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}",
            },
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "n": n,
                "stop": stop,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty,
                "logit_bias": logit_bias,
                "user": user,
            },
        )
        if r.status_code != 200:
            raise Exception(f"OpenAI API returned status code {r.status_code}: {r.text}")
        return r.json()

    return exponential_backoff(_fn)


model_registry.register(
    fn=openai_chat,
    collection_name="openai",
    id="openai-chat",
    description="Given a list of messages describing a conversation, the model will return a response.",
)
