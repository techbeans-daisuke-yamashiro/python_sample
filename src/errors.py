from typing import Optional, Tuple, List, Type


class ApiError(Exception):
    """ エラーの基底となるクラス """
    status_code: int = 400
    detail: str = 'API error'  # エラー概要

    def __init__(self, reason: Optional[str] = None):
        if reason:
            self.reason = reason

    def __str__(self):
        return f'{self.detail}\n{self.reason}'


class ItemNotFoundError(ApiError):
    status_code = 404
    detail={'Item Not Found'}


def error_response(error_types: List[Type[ApiError]]) -> dict:
    # error_types に列挙した ApiError を OpenAPI の書式で定義する
    d = {}
    for et in error_types:
        if not d.get(et.status_code):
            d[et.status_code] = {
                'description': f'"{et.detail}"',
                'content': {
                    'application/json': {
                        'example': {
                            'detail': et.detail
                        }
                    }
                }}
        else:
            # 同じステータスコードなら description へ追記
            d[et.status_code]['description'] += f'<br>"{et.detail}"'
    return d