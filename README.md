**This is a csv parsing tool built for AdLib CM purposes ONLY. It is not production ready and should only be used for internal guidance.**

**How it works:**
Python app with Streamlit frontend. Certain depends must be installed in order for tool to function\
This tool does not save any data\
The tool is setup to only run on localhost of the host device and will not be accessible on local networks unless a port if forwarded manually.\
Currently, the instructions are for Mac/Linux devices but theoretically this should also run on Windows machines.

**How to use:**
1. Install python
2. Although not absolutely neccessary, creating a virtual environment is recommended:
'''
python -m venv venv && source venv/bin/activate
'''
3. Install depends
'''
pip install -r requirements.txt
'''
4. Run
'''
streamlit run 0del.py
'''
5. App should open in a browser. If not, visit http://localhost:8501