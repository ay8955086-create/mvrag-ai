"""
Prompt builder for MVRAG AI.
"""

from __future__ import annotations


class PromptBuilder:
    """
    Builds prompts for Gemini.
    """

    @staticmethod
    def build(
        question: str,
        context: list[dict],
    ) -> str:

        context_text = "\n\n".join(
            item["document"]
            for item in context
        )

        return f"""
You are an AI assistant for answering questions about videos.

Use ONLY the context below.

If the answer is not available in the context,
say:

"I couldn't find that information in the video."

------------------------

CONTEXT

{context_text}

------------------------

QUESTION

{question}

------------------------

ANSWER
"""