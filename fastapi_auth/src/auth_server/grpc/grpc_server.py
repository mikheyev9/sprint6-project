import grpc

import src.auth_server.grpc.auth_pb2 as auth_pb2
import src.auth_server.grpc.auth_pb2_grpc as auth_pb2_grpc
from src.auth_server.abc.base import BaseAuthService


class GRPCAuthService(auth_pb2_grpc.AuthServiceServicer, BaseAuthService):

    def CheckToken(self, request, context):
        token = request.token
        result = self.check_token(token)
        return auth_pb2.CheckTokenResponse(**result.to_proto())

    async def serve(self):
        server = grpc.aio.server()
        auth_pb2_grpc.add_AuthServiceServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{self.port}')
        await server.start()
        await server.wait_for_termination()

    async def stop(self):
        if hasattr(self, "server"):
            await self.server.stop(5)
