import asyncio
import threading
from retoolrpc import RetoolRPC, RetoolRPCConfig
from TicketGenerator import TicketGenerator


class RPCServer:
    def __init__(self):
        self.rpc_config = RetoolRPCConfig(
            api_token="retool_01hz971zbvyz71dtpzzdjwmn1d",
            host="https://terio.retool.com",
            resource_id="7fc956fd-c01f-4913-9914-4baaf2d4bce9",
            environment_name="production",
            polling_interval_ms=1000,
            log_level="info",
        )
        self.rpc = RetoolRPC(self.rpc_config)
        self.register_methods()

    def register_methods(self):
        self.rpc.register(
            {
                "name": "imprimirTicket",
                "arguments": {
                    "id": {
                        "type": "string",
                        "description": "Id Pedido",
                        "required": True,
                        "array": False,
                    },
                    "calle": {
                        "type": "string",
                        "description": "Calle",
                        "required": True,
                        "array": False,
                    },
                    "colonia": {
                        "type": "string",
                        "description": "Colonia",
                        "required": True,
                        "array": False,
                    },
                    "cliente": {
                        "type": "string",
                        "description": "Cliente",
                        "required": True,
                        "array": False,
                    },
                    "monto": {
                        "type": "string",
                        "description": "Monto",
                        "required": True,
                        "array": False,
                    },
                    "status": {
                        "type": "string",
                        "description": "Status",
                        "required": True,
                        "array": False,
                    },
                    "contacto": {
                        "type": "string",
                        "description": "Telefono",
                        "required": True,
                        "array": False,
                    },
                    "fecha": {
                        "type": "string",
                        "description": "Fecha",
                        "required": True,
                        "array": False,
                    }
                },
                "implementation": self.obtener_datos,
                "permissions": None,
            }
        )

    def obtener_datos(self, args, context):
        try:
            id_pedido = args.get('id')
            cliente = args.get('cliente')
            calle = args.get('calle')
            colonia = args.get('colonia')
            monto = args.get('monto')
            status = args.get('status')
            telefono = args.get('contacto')
            fecha = args.get('fecha')
            self.imprimir_ticket(id_pedido, cliente, calle, colonia, monto, status, telefono, fecha)
        except Exception as e:
            print("Error al obtener datos:", str(e))

    def imprimir_ticket(self, id_pedido, cliente, calle, colonia, monto, status, telefono, fecha):
        try:
            print(f"Imprimiendo {id_pedido}...")
           
            ticket_generator = TicketGenerator(
                id_pedido=id_pedido,
                cliente=cliente,
                monto=monto,
                direccion=calle,
                colonia=colonia
            )
            ticket_generator.generar_ticket("ticket.pdf")
        except Exception as e:
            print(f"Error: {str(e)}")

    async def start(self):
        await self.rpc.listen()

    def run(self):
        asyncio.run(self.start())
