import requests

from django.conf import settings


def req_url(method, end, data=None):
    url = settings.VOTING_GITLAB['api_url'] + "/projects/" + settings.VOTING_GITLAB['project_id'] + end
    print(url)
    return getattr(requests, method)(
        url,
        headers={"PRIVATE-TOKEN": settings.VOTING_GITLAB['private_token']},
        data=data)
