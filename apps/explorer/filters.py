"""

pageable filter

"""
from rest_framework.filters import BaseFilterBackend
from django_filters import compat

class TxsQueryBackend(BaseFilterBackend):

    def filter_queryset(self, request, qs, view):
        return qs

    def get_schema_fields(self, view):
        return [
            compat.coreapi.Field(
                name='address',
                required=False,
                type="string",
                location='query',
                schema=compat.coreschema.String(
                    description="获取指定地址的交易列表"
                )
            ),
            compat.coreapi.Field(
                name='type',
                required=False,
                type="string",
                location='query',
                schema=compat.coreschema.String(
                    description="获取交易类型：in/out，与 address 配合使用"
                )
            ),
            compat.coreapi.Field(
                name='exclude_value_0',
                required=False,
                type="bool",
                location='query',
                schema=compat.coreschema.String(
                    description="排除交易额为0的交易，true 为排除，默认 false"
                )
            ),
            # TODO 暂不支持
            # compat.coreapi.Field(
            #     name='exclude_contract',
            #     required=False,
            #     type="bool",
            #     location='query',
            #     schema=compat.coreschema.String(
            #         description="排除发送给合约的交易，true为排除，默认 false"
            #     )
            # ),
            compat.coreapi.Field(
                name='block_hash',
                type="string",
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="获取指定区块哈希的交易列表"
                )
            ),
            compat.coreapi.Field(
                name='block_number',
                type="int",
                required=False,
                location='query',
                schema=compat.coreschema.String(
                    description="获取指定区块号的交易列表"
                )
            ),
        ]
