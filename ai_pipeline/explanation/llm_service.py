from typing import Dict
from backend.services.groq_client import get_groq_client, clean_thinking_tags
from backend.config import TEXT_MODELS
from ai_pipeline.explanation.prompts import ENGLISH_EXPLANATION_PROMPT, HINDI_EXPLANATION_PROMPT

class LLMExplanationService:
    def generate_bilingual_explanations(self, vlm_analysis: str, subject: str = "General Science") -> Dict[str, str]:
        """
        Generates both English and Hindi audio descriptions from VLM analysis.
        Returns: { "en": "...", "hi": "..." }
        """
        en_text = self._generate_explanation(vlm_analysis, subject, lang="en")
        hi_text = self._generate_explanation(vlm_analysis, subject, lang="hi")

        return {
            "en": en_text,
            "hi": hi_text
        }

    def _generate_explanation(self, vlm_analysis: str, subject: str, lang: str = "en") -> str:
        prompt_template = ENGLISH_EXPLANATION_PROMPT if lang == "en" else HINDI_EXPLANATION_PROMPT
        prompt = prompt_template.format(analysis=vlm_analysis, subject=subject)

        try:
            client = get_groq_client()
            for text_model in TEXT_MODELS:
                try:
                    response = client.chat.completions.create(
                        model=text_model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.4
                    )
                    text = clean_thinking_tags(response.choices[0].message.content)
                    if text:
                        return text
                except Exception as e:
                    print(f"Model '{text_model}' error during {lang} explanation generation: {e}")
        except Exception as e:
            print(f"LLM Explanation client error: {e}")

        # Structured fallback explanations if Groq call fails
        if lang == "en":
            return (
                f"This {subject} diagram illustrates key technical concepts. "
                "The visual layout displays data trends and structural components clearly labeled. "
                "Understanding these relationships highlights the fundamental principles of the topic."
            )
        else:
            return (
                f"यह {subject} आरेख मुख्य तकनीकी अवधारणाओं को दर्शाता है। "
                "दृश्य लेआउट डेटा प्रवृत्तियों और संरचनात्मक घटकों को स्पष्ट रूप से प्रस्तुत करता है। "
                "इन संबंधों को समझना इस विषय के मूलभूत सिद्धांतों को उजागर करता है।"
            )
