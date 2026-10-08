import os
import base64
import requests
from openai import OpenAI

# 🔑 आपका Nvidia NIM क्लाइंट सेटअप
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="******" 
)

def generate_leonardo_prompts(video_context):
    print("🤖 Nvidia NIM (Llama 3.3 70B) से प्रॉम्ट्स तैयार किए जा रहे हैं...")
    
  
prompt = f"""
You are an expert AI Video Prompt Engineer and Cinematographer. Your task is to analyze the given Video Context and break it down into exactly FOUR consecutive, highly-detailed visual prompts for AI video generation models. 
Each prompt represents a precise 5-second sequence of a 20-second total video.

Video Context to analyze:
"{video_context}"

⚠️ CORE RULES FOR GENERATING PROMPTS:
1. Output format requirement: Provide strictly 4 distinct prompts labeled with their exact timestamps:
   - [0-5 Seconds]
   - [5-10 Seconds]
   - [10-15 Seconds]
   - [15-20 Seconds]
2. Language: Write all prompts strictly in English.
3. Content restriction: Do not include any dialogue, narration text, or sound effects descriptions. Focus entirely on physical actions, character expressions, dynamic camera movements (e.g., tracking shot, slow pan, zoom), lighting style, and background environment.
4. Visual Consistency: Maintain 100% character and setting continuity across all 4 prompts (same main character appearance, consistent wardrobe, identical core environment).
5. Cinematic Enhancement: Conclude every single prompt with high-end production and quality keywords such as: "Cinematic, hyper-realistic, 8k resolution, highly detailed, dramatic studio lighting, photorealistic, professional color grading."

🎯 EXPECTED OUTPUT FORMAT:
[0-5 Seconds]: <detailed visual prompt>
[5-10 Seconds]: <detailed visual prompt>
[10-15 Seconds]: <detailed visual prompt>
[15-20 Seconds]: <detailed visual prompt>
"""

    try:
        response = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ टेक्स्ट जनरेशन में एरर आया: {str(e)}"


def generate_image_via_api(prompt_text, output_filename):
    print(f"🎨 Nvidia NIM (DeepSeek Janus Pro 7B) से इमेज बनाई जा रही है: {output_filename}...")
    
    # 💡 404 एरर से बचने के लिए हम सीधे सही API URL पर पोस्ट रिक्वेस्ट भेज रहे हैं
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": "****",
        "Content-Type": "application/json"
    }
    
    # Janus-Pro-7B के लिए सही फॉर्मेट जो इमेज जनरेट करता है
    payload = {
        "model": "deepseek/janus-pro-7b",
        "messages": [
            {
                "role": "user",
                "content": f"Generate an image based on this prompt: {prompt_text}"
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            # कुछ मॉडल्स टेक्स्ट रिपॉन्स में base64 इमेज देते हैं, या सीधे इमेज का डेटा देते हैं
            # चेक करते हैं कि क्या रिपॉन्स आया है
            content = result['choices'][0]['message']['content']
            
            # अगर रिपॉन्स में base64 डेटा है
            if "b64_json" in content or len(content) > 1000:
                # यहाँ हम मान रहे हैं कि डेटा आ गया, उसे सेव करेंगे
                print("✅ इमेज डेटा मिल गया! सेव किया जा रहा है...")
                # नोट: अगर यह सिर्फ टेक्स्ट दे रहा है, तो हमें मॉडल बदलना होगा
                with open(output_filename, "wb") as fh:
                    fh.write(base64.b64decode(content))
            else:
                print(f"🤖 मॉडल ने इमेज बनाने के बजाय यह कहा: {content}")
                print("💡 इसका मतलब Nvidia ने इस फ्री अकाउंट पर इमेज जनरेशन को पूरी तरह डिसेबल कर दिया है।")
        else:
            print(f"❌ सर्वर एरर: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ इमेज जनरेशन में एरर आया: {str(e)}")


# --- मुख्य प्रोग्राम (Main Execution) ---
if __name__ == "__main__":
    
    my_video_context = """
    एक व्यस्त सड़क पर एक बड़ा पत्थर गिरा हुआ है। कई लोग आ-जा रहे हैं और उससे बचकर निकल रहे हैं, 
    लेकिन कोई उसे हटा नहीं रहा। तभी एक लड़का (मुख्य पात्र) आता है, वह रुकता है और उस भारी पत्थर को 
    दोनों हाथों से उठाकर सड़क के किनारे सुरक्षित जगह पर रख देता है। पत्थर हटाने के बाद उसे सड़क पर 
    एक गिरा हुआ सोने का सिक्का चमकता हुआ दिखाई देता.
    """
    
    # 1. प्रॉम्ट्स स्क्रीन पर प्रिंट होंगे (जो आपको पहले ही मिल चुके हैं)
    # generated_prompts_text = generate_leonardo_prompts(my_video_context)
    
    # 2. अब हम आपके पहले सीन के प्रॉम्ट से सीधे इमेज बनाएंगे
    scene1_prompt = "A busy street with people walking in all directions, a large boulder in the middle of the road, camera angle is a wide shot from a slightly elevated position, lighting is natural daylight with a slight warm tone. Cinematic, hyper-realistic, 8k resolution, photorealistic."
    
    generate_image_via_api(scene1_prompt, "scene1.png")
