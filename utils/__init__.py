def make_response_data(data=None, code=1, message='ok'):
    """
    构造返回的响应数据
    :param data: 真正的数据
    :param code: 应用层面状态码
    :param message:
    :return: response_data -> dict
    """
    response_data = dict()
    response_data['code'] = code
    response_data['message'] = message
    response_data['data'] = data
    return response_data
