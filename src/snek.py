import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from io import StringIO
from contextlib import redirect_stdout
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()
bot_token = os.environ['BOT_TOKEN']  # xoxb-...
app_token = os.environ['SOCKET_TOKEN']  # xapp-...
signing_secret = os.environ['SIGNING_SECRET']

app = App(token=bot_token)


@app.event("app_mention")
def mention_handler(body, say):
	""" Respond to an @-mention directing to the slash command """
	say('Use /snek to open the interactive dialog.')


@app.command("/snek")
def slash_handler(ack, body, say):
	""" Show the input dialog box to the user """
	ack()
	handler.client.web_client.dialog_open(
		trigger_id=body['trigger_id'],
		dialog={
			"title": "Run some Python code!",
			"submit_label": "Submit",
			"callback_id": "run_code",
			"elements": [{
				"label": "Write code here:",
				"type": "textarea",
				"name": "raw_input",
				"placeholder": "Remember to print your output!",
			}]
		}
	)
# def slash_handler


@app.action("run_code")
def handle_run_code(ack, body, say):
	""" Takes input from the textbox, and executes the contained code """
	ack()
	# channel = body['channel']['id']
	input = body['submission']['raw_input']

	response_base = f"```{body['user']['name']} ran some python code!" \
		+ f"\n\n----- Input -----\n{input}"

	# make sure no dangerous input is passed
	if 'environ' in input or 'get_env' in input:
		say(
			response_base
			+ "\n\n----- Output -----\nAttempted to access secret information.  Denied.```"
		)
		return

	f = StringIO()
	with redirect_stdout(f):
		try:
			exec(input)
		except Exception as e:
			say(
				response_base
				+ f"\n\n----- Output -----\n{e}.```"
			)
			return

	say(
		response_base
		+ f"\n\n----- Output -----\n{f.getvalue()}```"
	)
# def handle_run_code


if __name__ == "__main__":
	handler = SocketModeHandler(app, app_token)
	handler.start()
