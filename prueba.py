import asyncio
from retoolrpc import RetoolRPC, RetoolRPCConfig
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


from TicketGenerator import TicketGenerator


async def start_rpc():
  rpc_config = RetoolRPCConfig(
      api_token="retool_01hz971zbvyz71dtpzzdjwmn1d",
      host="https://terio.retool.com",
      resource_id="7fc956fd-c01f-4913-9914-4baaf2d4bce9",
      environment_name="production",
      polling_interval_ms=1000, # optional version number for functions schemas
      log_level="info", # use 'debug' for more verbose logging
  )

  rpc = RetoolRPC(rpc_config)
  
  
  def obtenerDatos(args, context):
      
    try:
      id_pedido = args.get('id')
      cliente = args.get('cliente')
      calle=args.get('calle')
      colonia=args.get('colonia')
      monto=args.get('monto')
      status=args.get('status')
      telefono=args.get('contacto')
      fecha=args.get('fecha')
      imprimirTicket(id_pedido,calle,colonia,monto,cliente, status,telefono,fecha)
      
    except Exception as e:
        print ("Error al obtener datos") 
    

  def imprimirTicket(id_pedido,calle,colonia,monto,cliente, status,telefono,fecha):
    try:
     print(f"Imprimiendo {id_pedido}...")
     ticket_generator = TicketGenerator(
     id_pedido = id_pedido,
     cliente= cliente,
     monto=monto,
     direccion=calle+", "+colonia,
     )
     ticket_generator.generar_ticket("ticket.pdf")
    except Exception as e:
        print(f"Error: {str(e)}")
        
  rpc.register(
      {
          "name": "imprimirTicket",
          "arguments": {
              "id": {
                  "type": "string",
                  "description": "Id Pedido",
                  "required": True,
                  "array": False,
              },
              
              "calle":{
                  "type": "string",
                  "description": "Calle",
                  "required": True,
                  "array": False,
              },
              "colonia":{
                  "type": "string",
                  "description": "Colonia",
                  "required": True,
                  "array": False,
              },
              "cliente":{
                  "type": "string",
                  "description": "Cliente",
                  "required": True,
                  "array": False,
              },
              "monto":{
                  "type": "string",
                  "description": "Monto",
                  "required": True,
                  "array": False,
              },
              "status":{
                  "type": "string",
                  "description": "Statusg",
                  "required": True,
                  "array": False,
              },
              "contacto":{
                  "type": "string",
                  "description": "Telefono",
                  "required": True,
                  "array": False,
              },
              "fecha":{
                  "type": "string",
                  "description": "Fecha",
                  "required": True,
                  "array": False,
              }
          },
          "implementation": obtenerDatos,
          "permissions": None,
      }
  )
  
  await rpc.listen()

if __name__ == "__main__":
    try:
        asyncio.run(start_rpc())
    except Exception as e:
        print(f"Error: {str(e)}")