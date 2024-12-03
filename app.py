import pickle
from datetime import datetime
import streamlit as st


# Clase para manejar un contacto
class Contacto:
    """
    Representa un contacto con nombre, fecha de nacimiento y correo electrónico.
    """
    def __init__(self, nombre, fecha_nacimiento, email):
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.email = email

    def __repr__(self):
        return f"{self.nombre} ({self.fecha_nacimiento}) - {self.email}"


# Clase para gestionar la lista de cumpleaños
class GestorDeCumpleaños:
    """
    Gestiona contactos con fechas de cumpleaños.
    """
    def __init__(self, archivo_datos="cumpleaños.pkl"):
        self.archivo_datos = archivo_datos
        self.contactos = self.cargar_datos()

    def cargar_datos(self):
        """
        Carga los datos desde un archivo .pkl.
        """
        try:
            with open(self.archivo_datos, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def guardar_datos(self):
        """
        Guarda los datos en un archivo .pkl.
        """
        with open(self.archivo_datos, "wb") as f:
            pickle.dump(self.contactos, f)

    def agregar_contacto(self, nombre, fecha_nacimiento, email):
        """
        Agrega un nuevo contacto.
        """
        self.contactos.append(Contacto(nombre, fecha_nacimiento, email))
        self.guardar_datos()

    def proximos_cumpleaños(self):
        """
        Devuelve una lista de contactos ordenados por cumpleaños más cercano.
        """
        hoy = datetime.now().date()
        lista_cumpleaños = []
        for contacto in self.contactos:
            fecha_nacimiento = datetime.strptime(contacto.fecha_nacimiento, "%Y-%m-%d").date()
            proximo = fecha_nacimiento.replace(year=hoy.year)
            if proximo < hoy:
                proximo = proximo.replace(year=hoy.year + 1)
            dias_restantes = (proximo - hoy).days
            lista_cumpleaños.append((contacto, dias_restantes))
        return sorted(lista_cumpleaños, key=lambda x: x[1])

    def eliminar_contacto(self, nombre):
        """
        Elimina un contacto de la lista.
        """
        self.contactos = [c for c in self.contactos if c.nombre != nombre]
        self.guardar_datos()


# Interfaz en Streamlit
def main():
    st.title("Gestor de Cumpleaños 🎉")

    gestor = GestorDeCumpleaños()

    # Menú principal
    menu = ["Ver Próximos Cumpleaños", "Agregar Cumpleaños", "Eliminar Cumpleaños"]
    eleccion = st.sidebar.selectbox("Menú", menu)

    # Ver próximos cumpleaños
    if eleccion == "Ver Próximos Cumpleaños":
        st.subheader("Próximos Cumpleaños")
        proximos = gestor.proximos_cumpleaños()
        if not proximos:
            st.info("No hay cumpleaños registrados.")
        else:
            for contacto, dias in proximos:
                st.write(f"🎂 {contacto.nombre}: {dias} días restantes ({contacto.fecha_nacimiento})")

    # Agregar un nuevo cumpleaños
    elif eleccion == "Agregar Cumpleaños":
        st.subheader("Agregar Cumpleaños")
        nombre = st.text_input("Nombre:")
        fecha_nacimiento = st.date_input("Fecha de Nacimiento:", min_value=datetime(1900, 1, 1).date())
        email = st.text_input("Correo Electrónico:")

        if st.button("Agregar"):
            if nombre and email:
                gestor.agregar_contacto(nombre, fecha_nacimiento.strftime("%Y-%m-%d"), email)
                st.success(f"Cumpleaños de {nombre} agregado con éxito.")
            else:
                st.error("Por favor, completa todos los campos.")

    # Eliminar un cumpleaños
    elif eleccion == "Eliminar Cumpleaños":
        st.subheader("Eliminar Cumpleaños")
        nombres = [c.nombre for c in gestor.contactos]
        if nombres:
            nombre_a_eliminar = st.selectbox("Selecciona un contacto a eliminar:", nombres)
            if st.button("Eliminar"):
                gestor.eliminar_contacto(nombre_a_eliminar)
                st.success(f"Contacto {nombre_a_eliminar} eliminado con éxito.")
        else:
            st.info("No hay contactos registrados para eliminar.")

if __name__ == "__main__":
    main()
