import requests
import csv
import os
import datetime


URL = "https://api.github.com/repos/elastic/enhancements/issues"
HEADERS = {"Authorization": f"token {os.environ['GITHUB_AUTH']}"}
NUM_PAGES = 20
PER_PAGE = 100

OUTPUT_CSV = "/Users/alexandermarquardt/tmp/issues.csv"


def download_issues():
    header = ['Summary', 'Link', 'Date']

    with open(OUTPUT_CSV, 'w', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(header)
        for page in range(1, NUM_PAGES+1):
            params = {"labels": [":logstash"], "page": page, "per_page": PER_PAGE, "sort": "created", "direction": "desc",
                      "status": "open"}

            resp = requests.get(URL, headers=HEADERS, params=params)
            json_response = resp.json()

            print(f"****** PAGE {page}")
            for issue_iter in range(len(json_response)):
                issue_num = json_response[issue_iter]["number"]
                html_url = json_response[issue_iter]["html_url"]
                title = json_response[issue_iter]["title"]
                created_at = json_response[issue_iter]["created_at"]
                created_at = datetime.datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d')

                csv_data = [title, f"=HYPERLINK(\"{html_url}\", \"{issue_num}\")", created_at]
                writer.writerow(csv_data)


if __name__ == '__main__':
    download_issues()

