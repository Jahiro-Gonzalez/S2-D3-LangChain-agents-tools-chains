

## Que hace

- Tiene una lista simple llamada `faqs`.
- Tiene una funcion llamada `buscar_faq_universidad`.
- Esa funcion se usa como tool.
- El agente usa esa tool para responder preguntas.
- El agente guarda el historial de conversacion en la sesion para recordar el contexto.

## Instalar

```bash
pip install -r requirements.txt
```

## Configurar

Copia `.env.example` como `.env`.

En `.env` pon tu modelo de Groq y tu API key.

Ejemplo:

 
MODEL_ID=llama-3.1-8b-instant
GROQ_API_KEY=tu_api_key


## Ejecutar


python agente_simple.py


Preguntas de ejemplo:

 
Como hago mi inscripcion?
Donde pago la colegiatura?
No puedo entrar, olvide mi clave
Que horario tiene el soporte tecnico?
ejemplo 2
