import clients.commonclient as cc
from clients.commonclient import MODEL_WEIGHT_UPDATE_SERVICE_URL


def post_to_model_weight_update_service(request):
    return cc.send_request(MODEL_WEIGHT_UPDATE_SERVICE_URL, request)
