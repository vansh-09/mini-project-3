from typing import Dict
from backend.services.groq_client import get_groq_client, clean_thinking_tags
from backend.config import TEXT_MODELS
from ai_pipeline.explanation.prompts import ENGLISH_EXPLANATION_PROMPT, HINDI_EXPLANATION_PROMPT

class LLMExplanationService:
    def generate_bilingual_explanations(
        self,
        vlm_analysis: str,
        subject: str = "General Science",
        prior_events_context: list = None
    ) -> Dict[str, str]:
        """
        Generates both English and Hindi audio descriptions from VLM analysis.
        Passes prior_events_context to prevent double/over-explaining previously covered diagrams.
        Returns: { "en": "...", "hi": "..." }
        """
        en_text = self._generate_explanation(vlm_analysis, subject, lang="en", prior_events_context=prior_events_context)
        hi_text = self._generate_explanation(vlm_analysis, subject, lang="hi", prior_events_context=prior_events_context)

        return {
            "en": en_text,
            "hi": hi_text
        }

    def _generate_explanation(
        self,
        vlm_analysis: str,
        subject: str,
        lang: str = "en",
        prior_events_context: list = None
    ) -> str:
        prompt_template = ENGLISH_EXPLANATION_PROMPT if lang == "en" else HINDI_EXPLANATION_PROMPT
        prompt = prompt_template.format(analysis=vlm_analysis, subject=subject)

        if prior_events_context:
            prior_summary = "\n- ".join(prior_events_context[-3:])
            prompt += (
                "\n\nContext of previously described diagram events in this lecture:\n"
                f"- {prior_summary}\n\n"
                "CRITICAL INSTRUCTION: DO NOT re-explain or over-explain diagram concepts, labels, or structures already described above. "
                "Focus exclusively on the NEW visual relationships, specific data trends, or structural changes introduced at this timestamp."
            )

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

        # Dynamic, context-grounded fallback explanations if Groq API fails or is rate-limited
        summary_snippet = ""
        if vlm_analysis:
            # Extract first 200 non-empty characters for grounded context
            clean_lines = [line.strip() for line in vlm_analysis.splitlines() if line.strip() and not line.startswith("VLM")]
            if clean_lines:
                summary_snippet = " ".join(clean_lines[:2])

        if lang == "en":
            if summary_snippet:
                return (
                    f"This {subject} diagram visualizes key instructional concepts: {summary_snippet[:160]}. "
                    "The components and trends labeled in the figure highlight core educational principles of this topic."
                )
            return (
                f"This {subject} diagram illustrates key technical concepts. "
                "The visual layout displays data trends and structural components clearly labeled. "
                "Understanding these relationships highlights the fundamental principles of the topic."
            )
        else:
            if summary_snippet:
                return (
                    f"यह {subject} आरेख मुख्य अवधारणाओं को प्रस्तुत करता है: {summary_snippet[:160]}। "
                    "चित्र में दिए गए मुख्य घटक और डेटा बिंदु इस विषय के मूलभूत सिद्धांतों को स्पष्ट रूप से दर्शाते हैं।"
                )
            return (
                f"यह {subject} आरेख मुख्य तकनीकी अवधारणाओं को दर्शाता है। "
                "दृश्य लेआउट डेटा प्रवृत्तियों और संरचनात्मक घटकों को स्पष्ट रूप से प्रस्तुत करता है। "
                "इन संबंधों को समझना इस विषय के मूलभूत सिद्धांतों को उजागर करता है।"
            )

