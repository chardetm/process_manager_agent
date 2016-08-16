from django.shortcuts import render
import django.contrib.auth

from models import Op
from serializers import UserSerializer, OpSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = django.contrib.auth.get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        data2[u'ops'] = []
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OpViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Op.objects.all()
    serializer_class = OpSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    # Override to set the user of the request using the credentials provided to perform the request.
    def create(self, request, *args, **kwargs):
        data2 = {}
        for key in request.data:
            data2[key] = request.data[key]
        serializer = self.get_serializer(data=data2)
        serializer.is_valid(raise_exception=True)

        # Save in the database
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # @list_route()
    @detail_route(methods=['post'])
    def run_op(self, request, pk=None):
        from lib.mister_fs import MisterFs
        mister_fs = MisterFs()
        op = Op.objects.get(pk=pk)
        print(op)
        generated_script = """
#!/bin/bash;
set -x;
%s
        """ % (op.script)
        mister_fs.create_file("toto", generated_script)
        # op_id = request.data["id"]
        print("running op %s" % (op))
        return Response({"Hello"})

