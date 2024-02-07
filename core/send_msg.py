import http.client, urllib
from core.libs import get_logger


logger = get_logger('msglog')

def CallMe(var1, var2):
    host = "api.vm.ihuyi.com"
    sms_send_uri = "/webservice/voice.php?method=Submit"

    account = "VM16602014"
    password = "850c8414542377a18d537f8ea0f3a867"
    mobile = "19521465727"
    text = f"您的监控 {var1} 出现了 {var2} 的情况，请及时处理！"
    conn = http.client.HTTPConnection(host)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    conn.request("POST", sms_send_uri, params,
                 headers)
    rsp = conn.getresponse()

    logger.info(f"phone call send status : {rsp.status}")

def PushOver(msg):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": "ahu3vbg3f5caty87ahuf2w3ust8vxz",
        "user": "uhvz7u9xnpnpob75pjbakku1t7jk5q",
        "message":  {
            'title': f"{msg}",
        }


      }), { "Content-type": "application/x-www-form-urlencoded" })
    rsp = conn.getresponse()

    logger.info(f"msg send status : {rsp.status}")


if __name__ == "__main__":
    #CallMe('test23')
    PushOver("test123")


