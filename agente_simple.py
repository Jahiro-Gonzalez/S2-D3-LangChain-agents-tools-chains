
import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq


faqs = [
    {
        "tema": "inscripciones",
        "respuesta": "Las inscripciones se hacen desde el portal estudiantil.",
        "palabras": ["inscripcion", "inscripciones", "materias", "portal"],
    },
    {
        "tema": "pagos",
        "respuesta": "Los pagos se revisan en el portal financiero o en caja.",
        "palabras": ["pago", "pagos", "colegiatura", "caja"],
    },
    {
        "tema": "horario_soporte",
        "respuesta": "El soporte tecnico atiende de lunes a viernes, de 8:00 a 18:00.",
        "palabras": ["horario", "atencion", "atención", "soporte tecnico", "soporte técnico"],
    },
    {
        "tema": "soporte",
        "respuesta": "Para problemas de acceso debes levantar un ticket con soporte tecnico.",
        "palabras": ["soporte", "ticket", "contrasena", "clave", "acceso"],
    },
]


def buscar_faq_universidad(pregunta):
    pregunta = pregunta.lower()

    for faq in faqs:
        for palabra in faq["palabras"]:
            if palabra in pregunta:
                return faq["respuesta"]

    return "No encontre informacion sobre eso."


def crear_agente():

    ruta_env = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(ruta_env)

    modelo = os.getenv("MODEL_ID", "llama-3.1-8b-instant")
    groq_api_key = os.environ.get("GROQ_API_KEY", "").strip()

    if not groq_api_key or groq_api_key == "tu_groq_api_key":
        print(
            f"Configura GROQ_API_KEY en {ruta_env} o en la sesion actual de PowerShell."
        )
        print("Ejemplo: $env:GROQ_API_KEY=\"tu_clave_real\"")
        return None

    if modelo.startswith("groq:"):
        modelo = modelo.split("groq:", 1)[1]

    modelo_llm = ChatGroq(model=modelo, groq_api_key=groq_api_key)

    instrucciones = """
    Eres un asistente de una universidad.
    Responde en espanol.
    Si no tienes informacion concreta, dilo claramente y de forma breve.
    """

    agente = create_agent(
        model=modelo_llm,
        tools=[],
        system_prompt=instrucciones,
    )

    return agente


def main():
    agente = crear_agente()

    if agente is None:
        return

    historial = []

    print("Agente simple de universidad")
    print("Escribe salir para terminar")
    print()

    while True:
        pregunta = input("Tu: ")

        if pregunta.lower() == "salir":
            print("Agente: adios")
            break

        respuesta_faq = buscar_faq_universidad(pregunta)

        if respuesta_faq != "No encontre informacion sobre eso.":
            print("Agente:", respuesta_faq)
            historial.append({"role": "user", "content": pregunta})
            historial.append({"role": "assistant", "content": respuesta_faq})
            print()
            continue

        resultado = agente.invoke(
            {"messages": historial + [{"role": "user", "content": pregunta}]}
        )

        respuesta = resultado["messages"][-1].content
        print("Agente:", respuesta)
        historial.append({"role": "user", "content": pregunta})
        historial.append({"role": "assistant", "content": respuesta})
        print()


if __name__ == "__main__":
    main()
