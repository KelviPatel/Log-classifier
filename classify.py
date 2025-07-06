import re 
import google.generativeai as genai
from Training.LLM import LLM_classification
import joblib
from sentence_transformers import SentenceTransformer

model=joblib.load("model/linear_regression.joblib")
encoder=SentenceTransformer('all-MiniLM-L6-v2')

def regx_creator(msg):
    patterns={
        r"nova\.(osapi|metadata).*":'HTTP Status',
        r"nova\.compute.*":'Resource Usage',
        r"User User\d+ logged (out|in).*":'user action',
        r"Backup (started|ended) at.*":'System Notification',
        r"Backup completed successfully.":'System Notification',
        r"System updated to version.*":'System Notification',
        r"File data_\d+\.csv uploaded successfully by user User.*":'System Notification'}
    
    for pattern,value in patterns.items():
        if re.search(pattern,msg):
            return value
    return None

def classify(logs):
    d1={0:'Critical Error', 1:'Error',2:'Security Alert',3:'System Notification',4:'User Action'}
    labels=[]
    for source,msg in logs:
        value=regx_creator(msg)
        if value :
            labels.append(value)
        elif source=="LegacyCRM":
            labels.append(LLM_classification(msg))
        else : 
            X = encoder.encode([msg])  # convert to vector
            ans=model.predict(X)[0]
            result=labels.append(d1[ans]) 
    return labels


if __name__=="__main__":
    logs = [
        ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
        ("BillingSystem", "User 12345 logged in."),
        ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
        ("AnalyticsEngine", "Backup completed successfully."),
        ("ModernHR", "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1 RCODE  200 len: 1583 time: 0.1878400"),
        ("ModernHR", "Admin access escalation detected for user 9429"),
        ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
        ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."),
        ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality."),
        ("LegacyCRM", "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025")
    ]
    print(classify(logs))


