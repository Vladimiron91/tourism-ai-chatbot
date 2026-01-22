import os
from dotenv import load_dotenv
from openai import OpenAI

#Variablen aus der .env Datei

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Funktion Firmendaten:
def lade_wissen():
    """Holt die Infs aus der Textdatei
    Falls die Datei fehlt, gibts eine kurze Fehlermeldung zurück"""

    try:
        #utf-8 ist wegen den Umlaute öäü
        with open("firmendaten.txt", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Info nicht gefunden. Bitte prüfen!"

def tourismus_bot():
    print("--- Vladi (Ostsee-Camping) ist startklar ---")
    print("(Zum Beenden einfach 'exit' tippen)")

    #Camping-Infos
    kontext = lade_wissen()

    #Kuno soll vom Campingsplatz Zierow klingen
    messages = [
        {
            "role": "system",
            "content": (
                f"Du bist Vladi, der digitale Helfer vom Ostseecamping Zierow. "
                f"Sei freundlich, locker (Duzen ist okay) und nutze dieses Wissen: {kontext}. "
                f"Falls du mal keine Antwort in den Daten findest, bleib ehrlich "
                f"und verweise auf die Rezeption."
            )
        }
    ]

    #Chat-Loop
    while True:
        nutzer_fragen = input("Gast: ")

        #Abbruchbedinungen
        if nutzer_fragen.lower() in ['exit', 'ende', 'quit', 'конец']:
            print("Ciao, bis zum nächsten Mal!")
            break

        #Fragen in Verlauf
        messages.append({"role": "user", "content": nutzer_fragen})

        try:
            #Antwort von Op.AI
            anfrage = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            bot_antwort = anfrage.choices[0].message.content
            print(f"\nVladi: {bot_antwort}\n")

            #Save Antwort, damit der Bot den Faden nicht verliert
            messages.append({"role": "assistant", "content": bot_antwort})

        except Exception as e:
            #Beim Down Fall von API (z.b. Key abgelaufen oder nicht bezahlt ;))
            print((f"Ups, da gab es ein Problem: {e}"))

if __name__ == "__main__":
    # Programm START!
    tourismus_bot()