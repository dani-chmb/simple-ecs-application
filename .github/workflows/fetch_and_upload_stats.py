import requests
import time
import json
import os

# GitHub API details
GITHUB_API_URL = "https://api.github.com"
REPO_NAME = os.getenv('REPO_NAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# AWS CLoudwatch details
AWS_REGION = os.getenv('AWS_REGION')
NAMESPACE = os.getenv('NAMESPACE')

# Initialize CloudWatch client with specified region
client = boto3.client(
  'cloudwatch',
  aws_access_key_id = AWS_ACCESS_KEY_ID,
  aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
  region_name = AWS_REGION  
)


def fetch_issues_and_prs():
  # Headers for GitHub API request
  
  headers = {
    "Authorization":f"token {GITHUB_TOKEN}"
  }
  
  url_repo = f"{GITHUB_API_URL}/repos/amazreech/{REPO_NAME}"
  print(f"URL: {url}")
  
  while True:
    response_repo = requests.get(url, headers=headers)
    
    if response_repo.status_code == 200:
      repo_stats = response_repo.json()
      num_issues = repo_status.get('open_issues_count', 0)
      num_prs = repo_status.get('open_issues_count', 0)
      return num_issues, num_prs
      
    elif response_repo.status_code == 202:
      print("Got 202, Wating...")
      time.sleep(30)
      
    else:
      print(f"Failed to fecth data: {response_repo.status_code}")
      return None, None

def upload_metrics_to_cloudwatch(num_issues, num_prs):

  if num_issues is not None and num_prs is not None:
    # put metric data to CloudWatch
    response = cloudwatch.put_metric_data(
      Namespace = NAMESPACE,
      MetricData = [
        {
          'MetricName':'NumberOfIssues',
          'Value':num_issues,
          'Unit':'Count'
        },
        {
          'MetricName':'NumberOfPRs',
          'Value':num_prs,
          'Unit':'Count'
        }
      ]
    )
    print("Uploaded metrics to cloudwatch:", response)
  else:
    print("No metrics to Upload")

if __name__ == "__main__":
  num_issues, num_prs = fetch_issues_and_prs()
  upload_metrics_to_cloudwatch(num_issues, num_prs)
