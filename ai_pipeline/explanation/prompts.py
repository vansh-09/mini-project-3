ENGLISH_EXPLANATION_PROMPT = """
You are an expert accessibility tutor creating an audio narrative for visually impaired students.
Based on the following diagram analysis:
'''
{analysis}
'''

Subject/Topic Context: {subject}

Instructions:
1. Write a clear, engaging spoken educational description (3-5 sentences).
2. DO NOT say generic captions like 'this image shows a graph'. Explain the core scientific/mathematical concept, axes, key trends, or component functions.
3. Optimize sentence flow for spoken audio reading (Text-to-Speech).
"""

HINDI_EXPLANATION_PROMPT = """
आप दृष्टिबाधित छात्रों के लिए एक विशेषज्ञ सुलभता शिक्षक के रूप में ऑडियो विवरण तैयार कर रहे हैं।
निम्नलिखित आरेख विश्लेषण के आधार पर:
'''
{analysis}
'''

विषय / प्रसंग: {subject}

निर्देश:
1. 3 से 5 स्पष्ट वाक्यों में एक स्पष्ट, आकर्षक और शैक्षिक हिंदी ऑडियो विवरण लिखें।
2. केवल सामान्य विवरण न दें। मुख्य वैज्ञानिक या गणितीय अवधारणा, अक्षों (axes), प्रवृत्तियों (trends) और घटकों के अर्थ को समझाएं।
3. टेक्स्ट-टू-स्पीच (TTS) ऑडियो पढ़ने के लिए वाक्यों का प्रवाह सरल रखें।
"""
