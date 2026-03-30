import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv()


def _hyde_temperature() -> float:
    raw_value = os.getenv("AEBM_HYDE_TEMPERATURE", "0.0").strip()
    try:
        return float(raw_value)
    except ValueError:
        print(f"[WARN] Invalid AEBM_HYDE_TEMPERATURE='{raw_value}', using 0.0")
        return 0.0


class HydeGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=_hyde_temperature(),
            model_name=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
            api_key=os.getenv("GROQ_API_KEY"),
        )

    def generate_hypothetical_cvs(self, job_description: str) -> str:
        """
        Generate two synthetic profiles (FR and EN) for vector search expansion.
        """
        print("[HYDE] Generating hypothetical profiles...")

        prompt = ChatPromptTemplate.from_template(
            """
            Tu es un expert en recrutement international.
            Ton objectif est d'aider un moteur de recherche vectoriel a trouver le candidat ideal.

            OFFRE D'EMPLOI :
            {job_desc}

            TACHE :
            Redige DEUX profils "resumes" ideaux pour ce poste.
            1. Le premier profil doit etre redige en FRANCAIS professionnel.
            2. Le second profil doit etre redige en ANGLAIS professionnel.

            Utilise le jargon technique precis, les soft skills attendus et les mots-cles de l'industrie.
            N'invente pas de nom, juste le contenu : "Experience en...", "Expertise in...".

            FORMAT DE SORTIE :
            [PROFIL FR]
            ... contenu ...
            [PROFIL EN]
            ... content ...
            """
        )

        chain = prompt | self.llm
        result = chain.invoke({"job_desc": job_description})
        return result.content
