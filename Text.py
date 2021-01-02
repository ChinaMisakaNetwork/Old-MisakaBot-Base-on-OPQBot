import json
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cms.v20190321 import cms_client, models

def Check(msg):
    try: 
        cred = credential.Credential("AKIDidS9h8oWr9M3hCnghZK3nQSahHm6vJFE", "BpOuFS70ogTQRJ1jS9k8QkJmK8AFatG6") 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cms.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cms_client.CmsClient(cred, "ap-beijing", clientProfile) 
        req = models.TextModerationRequest()
        bs = str(base64.b64encode(msg.encode("utf-8")), "utf-8")
        params = {
            "Content": bs
        }
        req.from_json_string(json.dumps(params))
        resp = client.TextModeration(req) 
        Result=json.loads(resp.to_json_string())
        return(Result)
    except TencentCloudSDKException as err: 
        return(err)
