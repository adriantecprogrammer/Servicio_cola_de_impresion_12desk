from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO
import qrcode
import os
from dotenv import load_dotenv

class TicketGenerator:
    def __init__(self, id_pedido, monto,cliente,direccion):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.monto = monto
        self.direccion=direccion
        self.textos = [
            f"ID Pedido: {self.id_pedido}",
            f"Nombre: {self.cliente}",
            f"Monto: ${self.monto}",
            f"Direccion: {self.direccion}",
        ]
    
    def calcular_altura(self):
        altura_base = 60 * mm  # Altura mínima del ticket
        altura_por_linea = 10 * mm  # Altura por línea de texto
        altura_total = altura_base + (len(self.textos) * altura_por_linea)
        return altura_total

    def generar_ticket(self, archivo_pdf="ticket.pdf"):
     try:
        load_dotenv()
        altura_ticket = self.calcular_altura()
        
        size = os.getenv("ticketSize")
        size = float(size)
        
        c = canvas.Canvas(archivo_pdf, pagesize=(size * mm, altura_ticket))

        # Calcular la posición horizontal para centrar el título
        titulo_width = c.stringWidth("TICKET DE COMPRA", "Helvetica-Bold", 12)
        x_position_titulo = (size * mm - titulo_width) / 2

        c.setFont("Helvetica-Bold", 12)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x_position_titulo, altura_ticket - 15 * mm, "TICKET DE COMPRA")

        c.setFont("Helvetica", 10)
        y_position = altura_ticket - 25 * mm
        for texto in self.textos:
            c.drawString(5 * mm, y_position, texto)
            y_position -= 10 * mm

        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=2, border=1)
        qr.add_data("Id del pedido: " + self.id_pedido)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        qr_io = BytesIO()
        qr_image.save(qr_io, format='PNG')
        qr_io.seek(0)
        qr_reportlab = canvas.ImageReader(qr_io)

        # Calcular la posición horizontal para centrar el código QR
        qr_width = 30 * mm
        x_position_qr = (size * mm - qr_width) / 2

        c.drawImage(qr_reportlab, x_position_qr, y_position - 30 * mm, width=qr_width, height=qr_width)
        y_position -= 40 * mm

        c.setLineWidth(0.5)
        c.line(5 * mm, y_position, size * mm - 5 * mm, y_position)  # Línea que abarca toda la anchura del ticket
        y_position -= 5 * mm

        # Añadir texto de agradecimiento
        texto_agradecimiento = "¡Gracias por tu compra!"
        texto_width = c.stringWidth(texto_agradecimiento, "Helvetica-Bold", 10)
        x_position_texto = (size * mm - texto_width) / 2

        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_position_texto, y_position, texto_agradecimiento)

        c.showPage()
        c.save()
     except Exception as e:
        print(e)

     
        
