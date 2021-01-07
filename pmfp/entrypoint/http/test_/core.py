from schema_entry import EntryPoint

from ..core import http

"schema", type=str, required=True,
                        help="用于验证的json schema,可以是路径也可以是url")
    parser.add_argument("--serialization", type=str,
                        choices=("json",), default="json", help="请求的返回值序列化协议.默认json")
    parser.add_argument("-m", "--method", type=str,
                        choices=("GET", "POST", "PUT", "DELETE"), default="GET", help="请求的http方法")
    parser.add_argument("-a", "--auth", type=str,
                        help="认证字符串,多字段的使用,分隔")
    parser.add_argument("--auth_type", type=str,
                        choices=("basic", "digest", "jwt", "oauth1"), help="认证类型")
    parser.add_argument("-p", "--payload", type=str,
                        help="请求的负载,需要指定json文件")
    parser.add_argument("-t", "--payload_type", type=str,
                        choices=("form", "json", "url", "stream"), default="json", help="负载的类型")
    parser.add_argument("-s", "--stream", action="store_true",
                        help="返回是否为流")
    parser.add_argument("--verify", action="store_true",
                        help="https请求是否进行ssl验证")
    parser.add_argument("--cert", type=str,
                        help="指定一个本地证书用作客户端证书,如果是证书加key的形式,可以用','隔开")
    parser.add_argument("url", type=str,
                        help="请求的路径")
class Test(EntryPoint):
    """检查http请求返回的数据是否满足json schema定义的模式."""
    argparse_noflag = "url"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["schema","url"],
        "properties": {
            "schema":{
                "type": "string",
                "descrpition": "用于验证的json schema,可以是路径也可以是url"
            }
            "url": {
                "type": "string",
                "description": "要访问的http资源的地址"
            },
            "method": {
                "type": "string",
                "description": "访问资源的方法",
                "default": "GET",
                "enum": ["GET", "POST", "DELETE", "PUT"]
            },
            "requests": {
                "type": "integer",
                "description": "请求的总次数",
                "default": 100
            },
            "concurrency": {
                "type": "integer",
                "description": "并发量",
                "default": 10
            },
            "duration": {
                "type": "integer",
                "description": "间隔时间,单位s",
                "default": 0
            },
            "data": {
                "type": "string",
                "description": "请求的负载"
            },
            "ct": {
                "type": "string",
                "description": "请求的负载类型",
                "enum": ["text/plain", "application/json"],
                "default": "text/plain"
            },
            "quiet": {
                "type": "boolean",
                "description": "安静执行",
                "default": False
            },
            "config_file": {
                "type": "string",
                "description": "配置文件",
            }
        }
    }


http_test = http.regist_sub(Test)
