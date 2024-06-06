from tkinter import *

ventana = Tk()
ventana.geometry("600x400")
ventana.title("12Desk")

botonImprimir= Button(ventana, text="Imprimir")
#botonImprimir.place(relx=0.5, rely=0.3, relwidth=0.20, relheight=0.10)
botonImprimir.place(x=500, y=15, width=80, height=35)
botonImprimir.config(bg="black", fg="white")


ventana.mainloop()
