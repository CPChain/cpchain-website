"""

views

"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import BaseFilterBackend
from django_filters import compat

from apps.chain.db import cpchain_db

class EventPageableBackend(BaseFilterBackend):

    def filter_queryset(self, request, qs, view):
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='address',
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="收信人地址"
                )
            ),
            compat.coreapi.Field(
                name='limit',
                required=False,
                type="int",
                location='query',
                schema=compat.coreschema.String(
                    description="每页大小"
                )
            ),
            compat.coreapi.Field(
                name='offset',
                type="int",
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="从0开始"
                )
            ),
        ]


class MessageDAppView(viewsets.ViewSet):
    filter_backends = [EventPageableBackend]

    def list(self, request):
        addr:str = request.GET.get('address', '')
        limit:int = request.GET.get('limit', 10)
        offset:int = request.GET.get('offset', 0)
        if addr.strip() == '':
            raise ValueError('地址不能为空')
        dapp_events = cpchain_db['dapps_events']
        count = dapp_events.count_documents(
            {
                "event": "NewMessage",
                "args.to": addr
            }
        )
        r = dapp_events.aggregate([
            # event
            {
                "$match": {
                    "event": "NewMessage",
                    "args.to": addr,
                    "args.recvID": {
                        "$gt": int(offset),
                        "$lte": int(offset) + int(limit)
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "logIndex": 0,
                    "transactionIndex": 0,
                }
            }
        ])
        data = {
            "count": count,
            "results": list(r)
        }
        return Response(data)
