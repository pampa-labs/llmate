# LLMate 🧉

Enjoy brewing your LLM-SQL solution.

Welcome to the LLMate repository. This README will guide you on how to clone the repository and run the Streamlit app contained within it.

### Cloning the Repository
With Git installed, open a terminal or command prompt and run the following command:

```python
git clone https://github.com/pampa-labs/llmate.git
```

This will create a directory named llmate in your current working directory, containing all the contents of the repository.

### Installing Dependencies
Before you run the app, you need to install the required libraries. Navigate to the llmate directory and run:

```python
pip install -r requirements.txt
```
This command will install all the libraries listed in the requirements.txt file.

### Running the Streamlit App
With the dependencies installed, you're now ready to run the Streamlit app. Execute the following command:

```python
streamlit run Home.py
```
A new window or tab should open in your default web browser, displaying the Streamlit app.

Database Connection & OpenAI API Key
By default, you can connect to the Chinook database. If you'd like to connect to your own database, ensure it is either SQLite or MySQL, as only these dialects are currently supported.

To fully leverage the capabilities of LLMate, you'll need to provide your own OpenAI API key.

