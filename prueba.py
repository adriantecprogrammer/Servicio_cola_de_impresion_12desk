import asyncio
from retoolrpc import RetoolRPC, RetoolRPCConfig
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
import qrcode
from io import BytesIO
import webbrowser


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
      
   # Crear un nuevo archivo PDF con tamaño de ticket (A6)
    c = canvas.Canvas("ticket.pdf", pagesize=A6)

    # Establecer el tamaño de fuente y el color
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0, 0, 0)

    # Dibujar el encabezado del ticket
    c.drawString(5*mm, 140*mm, "--- TICKET DE COMPRA ---")

    # Dibujar los detalles del ticket
    c.setFont("Helvetica", 10)
    c.drawString(5*mm, 130*mm, f"ID Pedido: {id_pedido}")
    c.drawString(5*mm, 125*mm, f"Nombre: {cliente}")
    c.drawString(5*mm, 105*mm, f"Monto: ${float(monto):.2f}")
    c.drawString(5*mm, 120*mm, f"Calle: {calle}")
    c.drawString(5*mm, 115*mm, f"Colonia: {colonia}")
    c.drawString(5*mm, 110*mm, f"Teléfono: {telefono}")
    #c.drawString(5*mm, 105*mm, f"Status: {status}")
    #c.drawString(5*mm, 100*mm, f"Fecha: {fecha}")


    # Generar el código QR con el ID del pedido
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=2, border=1)
    qr.add_data("Id del pedido: "+ id_pedido)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Convertir la imagen del código QR a un objeto compatible con ReportLab
    qr_io = BytesIO()
    qr_image.save(qr_io, format='PNG')
    qr_io.seek(0)
    qr_reportlab = canvas.ImageReader(qr_io)

    # Dibujar el código QR en el ticket
    c.drawImage(qr_reportlab, 65*mm, 105*mm, width=30*mm, height=30*mm)

    # Dibujar línea separadora
    c.setLineWidth(0.5)
    c.line(5*mm, 100*mm, 95*mm, 100*mm)

    # Dibujar mensaje de agradecimiento
    c.setFont("Helvetica-Bold", 10)
    c.drawString(5*mm, 95*mm, "¡Gracias por su compra!")

    # Guardar el archivo PDF
    c.showPage()
    c.save()
    
    webbrowser.open("ticket.pdf")
    
    
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