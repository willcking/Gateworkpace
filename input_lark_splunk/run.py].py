import requests

url = "https://open.larksuite.com/open-apis/admin/v1/audit_infos?event_name=account_login&user_id_type=user_id"
payload = ''


headers = {
  'Authorization': 'Bearer t-g2072q1MHHGPXZVPXBWS65MOBNTWNVNZXFPQHN2O'
}

response = requests.request("GET", url, headers=headers, data=payload)

#print(response.json())
data = response.json()['data']['items']


for i in data:
    print(i)