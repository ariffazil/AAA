#!/usr/bin/env python3
"""
OpenClaw Channel Abstraction v1.0.0

Multi-channel interface for OpenClaw orchestrator.
Currently supports: Telegram (primary)
Future: Discord, WhatsApp, Web, Voice

Channel abstraction decouples the orchestrator brain from the transport layer.
Each channel adapter normalizes inbound messages to a common format and
denormalizes outbound responses to channel-specific format.

Forged: 2026-09-12 by 333-AGI under F13 directive
DITEMPA BUKAN DIBERI
"""

from __future__ import annotations

import json
import os
import time
import re
from typing import Any, Optional, Protocol
from dataclasses import dataclass, field, asdict
from enum import Enum


# ─── Channel Types ───────────────────────────────────────────────────────


class ChannelType(str, Enum):
    TELEGRAM = "telegram"
    DISCORD = "discord"
    WHATSAPP = "whatsapp"
    WEB = "web"
    A2A = "a2a"
    CLI = "cli"


@dataclass
class InboundMessage:
    """Normalized inbound message from any channel."""

    channel: ChannelType
    channel_msg_id: str
    chat_id: str
    person_id: str
    person_name: str = ""
    person_class: str = "unknown"  # SOVEREIGN | warga | unknown
    content: str = ""
    content_type: str = "text"  # text | voice | image | file
    media_url: str = ""
    reply_to: str = ""
    timestamp: float = 0
    language: str = "mixed"
    metadata: dict = field(default_factory=dict)


@dataclass
class OutboundMessage:
    """Normalized outbound message to any channel."""

    channel: ChannelType
    chat_id: str
    content: str = ""
    content_type: str = "text"  # text | voice | image | file | markdown
    reply_to: str = ""
    media_url: str = ""
    parse_mode: str = ""  # markdown | html
    disable_preview: bool = True
    metadata: dict = field(default_factory=dict)


class ChannelAdapter(Protocol):
    """Protocol for channel adapters."""

    def receive(self, raw: dict) -> InboundMessage:
        """Convert raw channel payload to normalized InboundMessage."""
        ...

    def send(self, message: OutboundMessage) -> dict:
        """Send normalized OutboundMessage to channel."""
        ...

    def health(self) -> dict:
        """Check channel health."""
        ...


# ─── Telegram Adapter ───────────────────────────────────────────────────


class TelegramAdapter:
    """Telegram channel adapter."""

    def __init__(self):
        self.bot_token = os.environ.get("OPENCLAW_TELEGRAM_TOKEN", "")
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}"

    def receive(self, raw: dict) -> InboundMessage:
        """Convert Telegram update to InboundMessage."""
        msg = raw.get("message", raw)
        chat = msg.get("chat", {})
        user = msg.get("from", {})

        content = msg.get("text", "")
        content_type = "text"
        media_url = ""

        # Handle different content types
        if msg.get("voice"):
            content_type = "voice"
            media_url = msg["voice"].get("file_id", "")
        elif msg.get("photo"):
            content_type = "image"
            media_url = msg["photo"][-1].get("file_id", "") if msg["photo"] else ""
        elif msg.get("document"):
            content_type = "file"
            media_url = msg["document"].get("file_id", "")

        # Detect language
        language = "mixed"
        if content:
            malay_chars = len(re.findall(r"[aeiou]", content.lower()))
            total_chars = len(re.findall(r"[a-z]", content.lower()))
            if total_chars > 0:
                if malay_chars / total_chars > 0.45:
                    language = "ms"
                else:
                    language = "en"

        return InboundMessage(
            channel=ChannelType.TELEGRAM,
            channel_msg_id=str(msg.get("message_id", "")),
            chat_id=str(chat.get("id", "")),
            person_id=str(user.get("id", "")),
            person_name=user.get("first_name", ""),
            person_class=self._classify_person(user.get("id", 0)),
            content=content,
            content_type=content_type,
            media_url=media_url,
            reply_to=str(msg.get("reply_to_message", {}).get("message_id", "")),
            timestamp=msg.get("date", time.time()),
            language=language,
            metadata={
                "username": user.get("username", ""),
                "chat_type": chat.get("type", ""),
            },
        )

    def send(self, message: OutboundMessage) -> dict:
        """Send message to Telegram."""
        import urllib.request
        import urllib.error

        if not self.bot_token:
            return {"success": False, "error": "No Telegram token configured"}

        method = "sendMessage"
        payload: dict[str, Any] = {
            "chat_id": message.chat_id,
            "text": message.content,
            "disable_web_page_preview": message.disable_preview,
        }

        if message.parse_mode:
            payload["parse_mode"] = message.parse_mode

        if message.reply_to:
            payload["reply_to_message_id"] = message.reply_to

        if message.content_type == "voice" and message.media_url:
            method = "sendVoice"
            payload["voice"] = message.media_url
            del payload["text"]

        url = f"{self.api_base}/{method}"
        try:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(
                url,
                data=data,
                method="POST",
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                return {"success": True, "message_id": result.get("result", {}).get("message_id")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def health(self) -> dict:
        """Check Telegram bot health."""
        import urllib.request

        try:
            url = f"{self.api_base}/getMe"
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read().decode())
                return {
                    "healthy": data.get("ok", False),
                    "bot_username": data.get("result", {}).get("username", ""),
                }
        except Exception as e:
            return {"healthy": False, "error": str(e)}

    def _classify_person(self, user_id: int) -> str:
        """Classify person by Telegram user ID."""
        SOVEREIGN_IDS = {267378578}
        WARGA_IDS = {1042200555, 764280302, 1024343313, 1237635275, 8410138119}

        if user_id in SOVEREIGN_IDS:
            return "SOVEREIGN"
        elif user_id in WARGA_IDS:
            return "warga"
        return "unknown"


# ─── Discord Adapter ────────────────────────────────────────────────────


class DiscordAdapter:
    """Discord channel adapter (stub — not yet wired)."""

    def __init__(self):
        self.token = os.environ.get("OPENCLAW_DISCORD_TOKEN", "")

    def receive(self, raw: dict) -> InboundMessage:
        return InboundMessage(
            channel=ChannelType.DISCORD,
            channel_msg_id=str(raw.get("id", "")),
            chat_id=str(raw.get("channel_id", "")),
            person_id=str(raw.get("author", {}).get("id", "")),
            person_name=raw.get("author", {}).get("username", ""),
            content=raw.get("content", ""),
            timestamp=time.time(),
        )

    def send(self, message: OutboundMessage) -> dict:
        return {"success": False, "error": "Discord adapter not yet wired"}

    def health(self) -> dict:
        return {"healthy": bool(self.token), "error": "Not wired" if not self.token else ""}


# ─── Channel Manager ────────────────────────────────────────────────────


class ChannelManager:
    """
    Manages multiple channel adapters.
    Routes inbound messages to the orchestrator and outbound responses back.
    """

    def __init__(self):
        self._adapters: dict[ChannelType, Any] = {}
        self._init_adapters()

    def _init_adapters(self):
        """Initialize available channel adapters."""
        self._adapters[ChannelType.TELEGRAM] = TelegramAdapter()
        self._adapters[ChannelType.DISCORD] = DiscordAdapter()
        # WhatsApp and Web are future — stub for now

    def receive(self, channel: ChannelType, raw: dict) -> InboundMessage:
        """Receive message from any channel."""
        adapter = self._adapters.get(channel)
        if not adapter:
            raise ValueError(f"No adapter for channel {channel}")
        return adapter.receive(raw)

    def send(self, message: OutboundMessage) -> dict:
        """Send message to any channel."""
        adapter = self._adapters.get(message.channel)
        if not adapter:
            return {"success": False, "error": f"No adapter for channel {message.channel}"}
        return adapter.send(message)

    def health(self) -> dict:
        """Check all channel health."""
        return {channel.value: adapter.health() for channel, adapter in self._adapters.items()}

    def get_adapter(self, channel: ChannelType) -> Any:
        """Get a specific channel adapter."""
        return self._adapters.get(channel)


# ─── Response Formatter ─────────────────────────────────────────────────


class ResponseFormatter:
    """
    Format orchestrator responses for different channels.
    Handles Telegram markdown, character limits, etc.
    """

    TELEGRAM_MAX_LENGTH = 4096

    @staticmethod
    def format_for_telegram(content: str, *, parse_mode: str = "Markdown") -> OutboundMessage:
        """Format content for Telegram."""
        # Truncate if too long
        if len(content) > ResponseFormatter.TELEGRAM_MAX_LENGTH:
            content = content[: ResponseFormatter.TELEGRAM_MAX_LENGTH - 20] + "\n\n[truncated]"

        return OutboundMessage(
            channel=ChannelType.TELEGRAM,
            chat_id="",  # Set by caller
            content=content,
            content_type="text",
            parse_mode=parse_mode,
            disable_preview=True,
        )

    @staticmethod
    def format_workflow_result(result: dict) -> str:
        """Format workflow result for human consumption."""
        lines = []
        lines.append(f"**Workflow: {result.get('name', 'unknown')}**")
        lines.append(f"Status: {result.get('state', 'unknown')}")
        lines.append(f"Duration: {result.get('duration_seconds', 0):.1f}s")
        lines.append("")

        for task in result.get("tasks", []):
            status_icon = {
                "completed": "✅",
                "failed": "❌",
                "skipped": "⏭️",
                "running": "🔄",
                "pending": "⏳",
            }.get(task.get("state", ""), "❓")

            lines.append(f"{status_icon} {task.get('id', '?')} → {task.get('agent', '?')}")
            if task.get("error"):
                lines.append(f"   Error: {task['error'][:100]}")

        return "\n".join(lines)

    @staticmethod
    def format_routing_decision(rule_id: str, target: str, confidence: float) -> str:
        """Format routing decision for logging/display."""
        return f"Route: {rule_id} → {target} (confidence: {confidence:.2f})"


# ─── Module-level singleton ─────────────────────────────────────────────
_manager: ChannelManager | None = None


def get_channel_manager() -> ChannelManager:
    """Get or create the singleton ChannelManager."""
    global _manager
    if _manager is None:
        _manager = ChannelManager()
    return _manager
