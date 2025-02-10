# Agent Workflow Framework

A modular framework for building agent-based workflows with configurable routing and validation.

##  Project Structure

```

## Virtual Environment Setup

To set up a virtual environment, follow these steps:

1. Create a virtual environment:

For Windows:
```batch
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Once the virtual environment is activated, install requirements:

If you have a requirements.txt file:
```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt file yet, you can create one by:
```bash
pip freeze > requirements.txt
```

To deactivate the virtual environment when you're done:
```bash
deactivate
```

Some helpful tips:
- Make sure you have Python installed on your system
- The virtual environment folder (venv) should be added to your .gitignore file
- You can confirm the virtual environment is activated by checking your command prompt - it should show (venv) at the beginning
- To see installed packages, use `pip list`