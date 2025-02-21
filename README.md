# 🦋 ChainFury

<img src="./docs/1.png" align="center"/>


ChainFury is a powerful tool that simplifies the creation and management of chains of prompts, making it easier to build complex chat applications using LLMs. With a simple GUI inspired by [LangFlow](https://github.com/logspace-ai/langflow), ChainFury enables you to chain components of [LangChain](https://github.com/hwchase17/langchain) together, allowing you to embed more complex chat applications with a simple JS snippet.

You can try out ChainFury [here](https://chainfury.nbox.ai/).


## Features
ChainFury supports a range of features, including:

- Recording all prompts and responses and storing them in a database
- Collecting metrics like latency to provide an easy-to-use scoring mechanism for end-users
- Querying OpenAI's API to obtain a rating for the response, which it stores in the database.
- [Plugins](./server/plugins/) to extend the functionality of ChainFury with callbacks

## Components
From the LangChain documentation, there are six main areas that LangChain is designed to help with. ChainFury consists of the same concepts to build LLM ChatBots. The components are, in increasing order of complexity:

| Glossary | LangChain    | ChainFury    |
| --- | --- | --- |
| 📃 LLMs and Prompts | Prompt management, prompt optimization, generic interface for all LLMs, and common utilities for working with LLMs   | Easy prompt management with GUI elements
| 🔗 Chains | Chains are sequences of calls (whether to an LLM or a different utility). LangChain provides a standard interface for chains, lots of integrations with other tools, and end-to-end chains for common applications | Easy chain management with GUI |
| 📚 Data Augmented Generation | Data Augmented Generation involves specific types of chains that first interact with an external datasource to fetch data to use in the generation step. Examples of this include summarization of long pieces of text and question/answering over specific data sources | Coming soon |
| 🤖 Agents | Agents involve an LLM making decisions about which Actions to take, taking that Action, seeing an Observation, and repeating that until done. LangChain provides a standard interface for agents, a selection of agents to choose from, and examples of end to end agents| Easy agent management with GUI |
| 🧠 Memory | Memory is the concept of persisting state between calls of a chain/agent. LangChain provides a standard interface for memory, a collection of memory implementations, and examples of chains/agents that use memory | Memory modules are supported, persistant memory coming soon |
| 🧐 Evaluation | [BETA] Generative models are notoriously hard to evaluate with traditional metrics. One new way of evaluating them is using language models themselves to do the evaluation. LangChain provides some prompts/chains for assisting in this | Auto evaluation of all prompts though OpenAI APIs |

---

<img src="./docs/2.png" align="center"/>

---
Installing ChainFury is easy, with two methods available.

### **Method 1: Docker**

The easiest way to install ChainFury is to use Docker. You can use the following command to run ChainFury:

```bash
docker build . -f Dockerfile -t chainfury:latest

docker run --env OPENAI_API_KEY=<your_key_here> -p 8000:8000 chainfury:latest
```

You can also pass a Database URL to the docker container using the `DATABASE_URL` environment variable. If you do not pass a database URL, ChainFury will use a SQLite database.

Example:

```bash
docker run -it -E DATABASE_URL="mysql+pymysql://<user>:<password>@127.0.0.1:3306/<database>" -p 8000:8000 chainfury
```

Now you can access the app on [localhost:8000](http://localhost:8000/ui/).

### **Method 2: Manual**

For this, you will need to build the frontend and and then run the backend. The frontend can be built using the following command:

```bash
cd client
yarn install
yarn build
```

To copy the frontend to the backend, run the following command:

```bash
cd ..
cp -r client/dist/ server/static/
mkdir -p ./server/templates
cp ./client/dist/index.html ./server/templates/index.html
```

Now you can install the backend dependencies and run the server. We recommend using Python 3.9 virtual environment for this:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd server
python3 -m uvicorn app:app --log-level=debug --host 0.0.0.0 --port 8000 --workers 1
```

<!-- collapsable -->

<details>
<summary>Script mode</summary>

Assuming you are in `server` directory, you can run the server using the following command:

```bash
python3 server.py --port 8000 --config_plugins='["echo"]'
```
</details>

Now you can access the app on [localhost:8000](http://localhost:8000/ui/).

---

<img src="./docs/3.png" align="center"/>

---

1. Start the server by using the docker file provided or by using the manual method.

2. Log into ChainFury by entering username = “admin” and password = “admin”

3. Click on create chatbot

4. Use one of the pre-configured chatbots or use the elements to create a custom chatbot.

5. Save & create your chatbot and start chatting with it by clicking the chat on the bottom-right. You can see chatbot statistics and feedback metrics in your ChainFury dashboard.

---

<img src="./docs/4.png" align="center"/>

---
ChainFury is a work in progress, and is currently in the alpha stage. Please feel free to contribute to the project in any form!

