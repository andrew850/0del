**This is a csv parsing tool built for AdLib CM purposes ONLY. It is not production ready and should only be used for internal guidance.**

**How to use:**
1. Visit: 0-delivery-report.streamlit.app
2. Download latest pacing report from email and drag or upload to the app

**How it works:**
* First, checks for all rows where Yesterday Spend = 0
* Filters out campaigns where:
    * End Date is in the past
    * Start Date is in the future or today
    * Campaign Status is set to off
    * If the answer is no to all the above,
* Flags Active Campaigns with Zero Spend (Needs Attention)
    * From these, flags any that have not delivered at all are flagged as critical

**Limitations**
* This tool has no connection to AdLib or any DSPs, it can only parse our specific csv pacing reports that are sent daily via email. 
* The tool does not save any data, closing the page clears the dashboard.


**How it works, technically:**
* Python app with Streamlit frontend. Two Depends must be installed in order for tool to function
    * streamlit, panda
* This tool does not save any data
* The tool is setup to only run on localhost and will not be accessible on local networks unless a port is forwarded manually. In the case of this github repo, it is hosted on Streamlit Cloud.
* These instructions are for Mac/Linux devices but theoretically this should also run on Windows machines.

**How to run locally:**
1. Install python
2. Although not absolutely neccessary, creating a virtual environment is recommended:
```
python -m venv venv && source venv/bin/activate
```
3. Install depends
```
pip install -r requirements.txt
```
4. Run
```
streamlit run 0del.py
```
5. App should open in a browser. If not, visit http://localhost:8501