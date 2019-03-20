import clients.commonclient as cc
from clients.commonclient import SINGLE_VIEW_RELATIVE_URL, MULTI_VIEW_RELATIVE_URL
from common.userparameters import UserParameters


def post_to_single_view(request):
    url = str(UserParameters().get_cloud_ip()) + SINGLE_VIEW_RELATIVE_URL
    return cc.send_request(url, request)


def post_to_multi_view(request):
    url = str(UserParameters().get_cloud_ip()) + MULTI_VIEW_RELATIVE_URL
    return cc.send_request(url, request)
