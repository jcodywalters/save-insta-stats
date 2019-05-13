# Lambda - Save Instagram Stats

#### A python script that saves an Instagram account's daily follower count to a Google Sheet. The lambda is configured to run daily using an AWS Event trigger.

Prerequisites:
- Google Account 
- Google Service Account Credentials
- AWS Account
- Instagram Auth Token
- Python 2/3

Note
- Save your Google Service Account inside the root folder. Call this file `sa-creds.json`
- To run this locally, you will need to supply the `ACCESS_TOKEN` and `SHEET_NAME` environment variables.

TO-DO
- Cloudformation script
- Caputure Post Insight data