import markovify
from flask import Flask
from twilio.twiml.messaging_response import Message, MessagingResponse

from get_giphy import get_giphy

app = Flask(__name__)


@app.route("/message", methods=["GET", "POST"])
def message():
    response = MessagingResponse()
    message = Message()
    sms_text = model.make_short_sentence(200)
    message.body(sms_text)
    gif_url = get_giphy(
        person_name="Donald Trump", tweet=sms_text, gif_type="downsized_still"
    )
    message.media(gif_url)

    response.append(message)

    return str(response)


if __name__ == "__main__":
    with open("tweets.csv") as f:
        text = f.read()

    model = markovify.Text(text)
    app.run(debug=True, port=5000)  # run app in debug mode on port 5000
