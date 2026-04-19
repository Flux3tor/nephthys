from nephthys.transcripts.transcript import Transcript


class Haj4ever(Transcript):
    """Transcript for Haj4ever."""

    program_name: str = "Haj4ever"
    program_owner: str = "U0A6A0J7UE6"  # @flux3tor

    help_channel: str = "C0ATMEQQ60K"  # #haj4ever-help
    ticket_channel: str = "C0ATEBMBSMV"  # #haj4ever-tickets
    team_channel: str = "C0AUQ3JQP96"  # #haj4ever-support-team

    faq_link: str = "https://hackclub.enterprise.slack.com/docs/T0266FRGM/F0AUN2BU4GG"
    identity_help_channel: str = "C092833JXKK"  # #identity-help

    first_ticket_create: str = f"""
:rac_info: Hey there (user), and welcome to help channel for Haj4ever! While we wait for someone to help you out, I have a couple of requests for you:
• Take a look through <{faq_link}|*the FAQ*> – you may find a solution waiting there for you
• If you have the answer to your question, hit that green button below!
"""
    ticket_create: str = f"""
:rac_info: Ah, hello there, fellow hack clubber! While we wait for a very nice human to come and help you out, I've been told to remind you to:
• Have a read of <{faq_link}|*the FAQ*> – it might have the answer you're looking for
• Once your question is (hopefully) answered, hit the button below!
"""
    ticket_resolve: str = f"""
Oh, :yayayayayay: ! This post has just been marked as resolved by <@{{user_id}}>! I'll go away and do whatever bots do now, \
but if you need any more help, just send another message in <#{help_channel}> and I'll be right back for you o/
"""

    faq_macro: str = f"""
Hi (user), this question is already answered in our FAQ! Here's the link again: <{faq_link}|*Haj4ever FAQ*>.

_I've marked this question as resolved for you, so please start a new thread if you need more help_
"""
    identity_macro: str = f"""
Hi (user), please could you ask questions about identity verification in <#{identity_help_channel}>? :rac_cute:

It helps the verification team keep track of questions easier!

_I've marked this thread as resolved btw!_
"""
    redirect_macro: str = "Oh! I will now tell the big boss people to come help you! (usergroup)"
    fraud_macro: str = """
Hi (user), would you mind directing any fraud related queries to <@U091HC53CE8>? :rac_cute:

It'll keep your case confidential and make it easier for the fraud team to keep track of!

_I've marked this thread as resolved btw!_
"""

    not_allowed_channel: str = f"hey, it looks like you're not supposed to be in that channel, pls talk to <@{program_owner}> if that's wrong"

    ship_cert_queue_macro: str | None = (
        "Hey (user), we currently have a backlog of projects waiting to be reviewed. Please be patient but we will be with you ASAP!\n>!"
    )