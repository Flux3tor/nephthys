import asyncio
import logging
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from slack_sdk.errors import SlackApiError

from nephthys.utils.env import env
from nephthys.utils.logging import send_heartbeat
from prisma.enums import TicketStatus


async def check_unclosed_tickets():
    """
    Checks for tickets that have been open for more than 24 hours.
    If any exist, pings the user group in the heartbeat channel.
    """

    try:
        # Get tickets that are not closed
        unclosed_tickets = await env.db.ticket.find_many(
            where={"NOT": [{"status": TicketStatus.CLOSED}]},
        )

        tickets_over_24h = []
        now = datetime.now(tz=timezone.utc)

        for ticket in unclosed_tickets:
            # Slack timestamps are in seconds
            ticket_time = datetime.fromtimestamp(float(ticket.msgTs), tz=timezone.utc)
            if (now - ticket_time) > timedelta(hours=24):
                tickets_over_24h.append(ticket)

        if tickets_over_24h:
            user_group_id = env.slack_user_group
            user_group_ping = f"<!subteam^{user_group_id}>"
            message = f"{user_group_ping} There are {len(tickets_over_24h)} tickets that have been open for more than 24 hours!"

            # Ping in heartbeat channel
            if env.slack_heartbeat_channel:
                await env.slack_client.chat_postMessage(
                    channel=env.slack_heartbeat_channel,
                    text=message
                )

            logging.info(f"Found {len(tickets_over_24h)} tickets over 24 hours. Pinged heartbeat channel.")

    except Exception as e:
        logging.error(f"Error checking unclosed tickets: {e}")
        await send_heartbeat(f"Error checking unclosed tickets: {e}")
