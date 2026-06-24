import requests

  API_KEY = "sk_71c423b81910b9719b4d55c6848e9fef043039f775ce1f6e"
  VOICE_ID = "2UVVG78koJmSOKFywat7"

  text = (
      "AI seekhna mushkil nahi hai, sirf ek barrier hai, starting, "
      "jo aaj shuru karte hain, 30 din baad woh alag hi jagah hote hain"
  )

  response = requests.post(
      f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
      headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
      json={
          "text": text,
          "model_id": "eleven_multilingual_v2",
          "voice_settings": {
              "stability": 0.68,
              "similarity_boost": 0.82,
              "style": 0.12,
              "use_speaker_boost": False
          }
      }
  )

  with open("t01_voice.mp3", "wb") as f:
      f.write(response.content)

  print("Saved: t01_voice.mp3")