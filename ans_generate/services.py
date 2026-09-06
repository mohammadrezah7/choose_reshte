from django.conf import settings


class AIServiceError(Exception):
    """هر خطای مربوط به فراخوانی سرویس هوش مصنوعی."""


def call_ai(prompt: str) -> str:
    provider = getattr(settings, "AI_PROVIDER", "anthropic")

    if provider == "openai":
        return _call_openai(prompt)

    if provider == "anthropic":
        return _call_anthropic(prompt)

    raise AIServiceError(f"مقدار AI_PROVIDER نامعتبر است: {provider!r}")


def _call_anthropic(prompt: str) -> str:
    try:
        import anthropic
    except ImportError as exc:
        raise AIServiceError(
            "t"
        ) from exc

    api_key = getattr(settings, "ANTHROPIC_API_KEY", "")
    if not api_key:
        raise AIServiceError("ANTHROPIC_API_KEY تنظیم نشده است.")

    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model=getattr(settings, "ANTHROPIC_MODEL", "claude-sonnet-4-5"),
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:
        raise AIServiceError(f"خطا در ارتباط با Anthropic API: {exc}") from exc

    return "".join(
        block.text for block in response.content if hasattr(block, "text")
    )


def _call_openai(prompt: str) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise AIServiceError(
            "t"
        ) from exc

    api_key = getattr(settings, "OPENAI_API_KEY", "")
    if not api_key:
        raise AIServiceError("OPENAI_API_KEY تنظیم نشده است.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
    except Exception as exc:
        raise AIServiceError(f"خطا در ارتباط با OpenAI API: {exc}") from exc

    return response.choices[0].message.content