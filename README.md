# AWS-Automation-with-Lambda-Boto3-

***********************************Assignment1:Automated S3 Bucket Cleanup***********************************

Discussion point (include in your documentation):In production, S3 Lifecycle Rules handle this natively with zero code. Explain in 2–3 lines when you'd use Lambda instead 

Answer:

If it’s just 'delete everything older than 30 days,' S3 Lifecycle Rules handle that out of the box with zero code. But if I need to delete only .log files with a specific metadata tag, verify against a database before deleting, or send a Slack alert when it happens—that’s where Lambda steps in



***********************************Assignment2:Automated EBS Snapshot Creation and Cleanup***********************************

Discussion point: AWS Data Lifecycle Manager (DLM) does this natively. Note in your documentation when Lambda is still the better choice

Answer:
DLM works great for simple 'take a snapshot every day and keep it for 30 days' policies. But if we need to send those snapshots to a completely separate AWS account for disaster recovery, apply custom tags dynamically based on environment conditions, or trigger an alert on failure—Lambda gives us full control over the process.


***********************************Assignment3:Auto-Tagging EC2 Instances on Launch***********************************

No discussion point mentioned in the assignment.




***********************************Assignment4:Daily AWS Cost Alert Using Cost Explorer API and SNS***********************************

Discussion point: Mention AWS Budgets as the managed alternative and when custom Lambda logic wins (per-service breakdowns, Slack/Teams delivery, anomaly logic).

Answer:

AWS Budgets is great if we just want a standard email when your bill crosses 80% of a target. But if you want a daily automated summary sent to a Slack channel breaking down spend by specific services, or custom logic that flags sudden cost anomalies in real time, a Lambda function reading cost data gives you complete control.


In iampolicy.json file, modify "Resource" with your respective ARN.
