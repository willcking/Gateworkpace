import lark_oapi as lark
import json
from requests_toolbelt import MultipartEncoder


# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
def main():
    # 创建client
    client = lark.Client.builder() \
        .app_id("YOUR_APP_ID") \
        .app_secret("YOUR_APP_SECRET") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    json_str = "{\"app_id\":\"cli_slkdjalasdkjasd\",\"app_secret\":\"dskLLdkasdjlasdKK\"}"
    body = json.loads(json_str)
    request: lark.BaseRequest = lark.BaseRequest.builder() \
        .http_method(lark.HttpMethod.POST) \
        .uri("/open-apis/auth/v3/tenant_access_token/internal") \
        .token_types({lark.AccessTokenType.TENANT}) \
        .body(body) \
        .build()

    # 发起请求
    response: lark.BaseResponse = client.request(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.request failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    # 处理业务结果
    lark.logger.info(str(response.raw.content, lark.UTF_8))


if __name__ == "__main__":
    main()
