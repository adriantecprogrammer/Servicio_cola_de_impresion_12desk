import asyncio
from retoolrpc import RetoolRPC, RetoolRPCConfig

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

  def helloWorld(args, context):
      return f"id de la orden: {args['name']}"

  rpc.register(
      {
          "name": "helloWorld",
          "arguments": {
              "name": {
                  "type": "string",
                  "description": "Your name",
                  "required": True,
                  "array": False,
              },
          },
          "implementation": generar_ticket,
          "permissions": None,
      }
  )

  await rpc.listen()

if __name__ == "__main__":
  asyncio.run(start_rpc())


def generar_ticket(nombre, cantidad, monto, direccion, telefono):
    # Crear un nuevo archivo PDF
    c = canvas.Canvas("ticket.pdf", pagesize=letter)

    # Establecer el tamaño de fuente y el color
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0, 0, 0)

    # Dibujar el encabezado del ticket
    c.drawString(50, 700, "--- TICKET DE COMPRA ---")

    # Dibujar los detalles del ticket
    c.setFont("Helvetica", 12)
    c.drawString(50, 650, f"Nombre del cliente: {nombre}")
    c.drawString(50, 625, f"Cantidad: {cantidad}")
    c.drawString(50, 600, f"Monto final: ${monto:.2f}")
    c.drawString(50, 575, f"Dirección: {direccion}")
    c.drawString(50, 550, f"Teléfono: {telefono}")

    # Guardar el archivo PDF
    c.showPage()
    c.save()

# Ejemplo de uso
nombre_cliente = "Juan Pérez"
cantidad_productos = 5
monto_final = 150.75
direccion_cliente = "Calle Principal 123"
telefono_cliente = "555-1234"

generar_ticket(nombre_cliente, cantidad_productos, monto_final, direccion_cliente, telefono_cliente)
    