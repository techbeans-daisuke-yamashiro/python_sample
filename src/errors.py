from typing import Optional, Tuple, List, Type
from fastapi import status, Response, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback

#カスタムAPIエラーの基底となるクラス
class ApiException(Exception):
    defaut_status_code: int = status.HTTP_400_BAD_REQUEST
    defaut_message: str = 'Bad Request'

    def __init__(self,
            status_code:Optional[int]=defaut_status_code,
            message:Optional[str]=defaut_message) -> None:
        self.nessage = message
        self.status_code = status_code
        self.detail ={'error': {'status_code': status_code, 'message': message}}

#システムIエラーの基底となるクラス
class SystemExeption(Exception):
    def __init__(self, e:Exception) -> None:
        self.exception = e
        self.stack_trace = traceback.format_exc()
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = {
            'error': {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': 'system error.'}}

class HttpRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
        except ApiException as ae:
            response = JSONResponse(ae.detail, status_code=ae.status_code)
        except Exception as e:
            se = SystemExeption(e)
            response = JSONResponse(se.detail,status_code=se.status_code)
        return response

def extract_errors(exceptions: List[Exception]) -> dict:
    data ={}
    for e in exceptions:
        e = dict(e.detail)['error']
        s = e['status_code']
        m = e['message']
        if data.get(s) is None:
            data[s]={'description': m}
        else:
            data[s]['description'] += f'<br>{m}'
    return data

def extract_system_exeption(e:SystemExeption = SystemExeption(Exception)):
    return { e.status_code: {'description':{e.detail['error']['message']}}}
    