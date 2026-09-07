"""
لایه‌ی انتزاعی فراخوانی سرویس هوش مصنوعی.
بسته به مقدار settings.AI_PROVIDER ("anthropic" یا "openai")،
درخواست به سرویس مناسب فرستاده می‌شود.

نکته درباره‌ی OpenRouter:
OpenRouter با API رسمی OpenAI سازگار است، فقط باید:
  1) OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
  2) OPENAI_MODEL با پیشوند ارائه‌دهنده نوشته شود، مثلاً "openai/gpt-4o-mini"

نیازمندی‌ها:
    pip install openai
    pip install anthropic   (فقط اگر از Anthropic استفاده می‌کنید)
"""

from django.conf import settings


class AIServiceError(Exception):
    """هر خطای مربوط به فراخوانی سرویس هوش مصنوعی."""


def call_ai(system_prompt: str, user_message: str) -> str:
    provider = getattr(settings, "AI_PROVIDER", "openai")

    if provider == "openai":
        return _call_openai(system_prompt, user_message)

    if provider == "anthropic":
        return _call_anthropic(system_prompt, user_message)

    raise AIServiceError(f"مقدار AI_PROVIDER نامعتبر است: {provider!r}")


def _call_openai(system_prompt: str, user_message: str) -> str:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise AIServiceError(
            "بسته‌ی openai نصب نیست. دستور 'pip install openai' را اجرا کنید."
        ) from exc

    api_key = getattr(settings, "OPENAI_API_KEY", "")
    if not api_key:
        raise AIServiceError("OPENAI_API_KEY تنظیم نشده است.")

    # برای OpenRouter باید این مقدار "https://openrouter.ai/api/v1" باشد.
    base_url = getattr(settings, "OPENAI_BASE_URL", "") or None

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = OpenAI(**client_kwargs)

    extra_headers = {}
    site_url = getattr(settings, "OPENROUTER_SITE_URL", "")
    site_name = getattr(settings, "OPENROUTER_SITE_NAME", "")
    if site_url:
        extra_headers["HTTP-Referer"] = site_url
    if site_name:
        extra_headers["X-Title"] = site_name

    try:
        response = client.chat.completions.create(
            model=getattr(settings, "OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            max_tokens=getattr(settings, "AI_MAX_TOKENS", 6000),
            temperature=getattr(settings, "AI_TEMPERATURE", 0.3),
            extra_headers=extra_headers or None,
        )
    except Exception as exc:
        raise AIServiceError(
            f"خطا در ارتباط با OpenAI/OpenRouter API: {exc}"
        ) from exc

    return response.choices[0].message.content


def _call_anthropic(system_prompt: str, user_message: str) -> str:
    try:
        import anthropic
    except ImportError as exc:
        raise AIServiceError(
            "بسته‌ی anthropic نصب نیست. دستور 'pip install anthropic' را اجرا کنید."
        ) from exc

    api_key = getattr(settings, "ANTHROPIC_API_KEY", "")
    if not api_key:
        raise AIServiceError("ANTHROPIC_API_KEY تنظیم نشده است.")

    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model=getattr(settings, "ANTHROPIC_MODEL", "claude-sonnet-4-5"),
            max_tokens=getattr(settings, "AI_MAX_TOKENS", 6000),
            temperature=getattr(settings, "AI_TEMPERATURE", 0.3),
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
    except Exception as exc:
        raise AIServiceError(f"خطا در ارتباط با Anthropic API: {exc}") from exc

    return "".join(
        block.text for block in response.content if hasattr(block, "text")
    )