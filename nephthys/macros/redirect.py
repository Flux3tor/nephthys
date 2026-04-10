from nephthys.macros.types import Macro
from nephthys.utils.env import env
from nephthys.utils.ticket_methods import reply_to_ticket


class Redirect(Macro):
    name = "redirect"
    aliases = ["admin"]

    async def run(self, ticket, helper, **kwargs) -> None:
        """
        A macro that pings the big boss people (user group).
        """
        user_group_id = env.slack_user_group
        user_group_ping = f"<!subteam^{user_group_id}>"

        await reply_to_ticket(
            text=env.transcript.redirect_macro.replace("(usergroup)", user_group_ping),
            ticket=ticket,
            client=env.slack_client,
        )
