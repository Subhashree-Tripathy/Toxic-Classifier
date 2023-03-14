import flask
from data import user_data
from services import lang_detect, sentiment_detect
import toxic_server_multilang as ts

app: flask.Flask = flask.Flask(__name__)


def default(args,filename):
    data_slice = None
    if args[0]:
        data_slice = user_data[0]
    
    elif args[1]:
        data_slice = user_data[1]

    elif args[2]:
        data_slice = user_data[2]
    if flask.request.method == "POST":
        data = flask.request.form
        comment = data.get("comment")
        print(comment)
        lang = lang_detect(comment)
        print(lang)
        sent = sentiment_detect(comment)
        print(sent)
        toxic = ts.predict(comment)
        data_slice.append(
                dict(
                    lang=lang,
                    sent=sent,
                    toxic="Toxic" if toxic==1 else "Non-toxic",
                    comment=comment,
                )
            )

    return flask.render_template(
        "home.html",
        userdata=data_slice,
        twitter=args[0],
        amazon=args[1],
        insta=args[2],
        filename = filename
    )


@app.route("/", methods=["GET", "POST"])
def twitter():
    return default([True, False, False],"twit.png")


@app.route("/amazon", methods=["GET", "POST"])
def amazon():
    return default([False, True, False],"ama.png")


@app.route("/insta", methods=["GET", "POST"])
def insta():
    return default([False, False, True],"mod.jpeg")

@app.route("/static/<filename>", methods=["GET"])
def images(filename):
    return flask.send_from_directory("static",filename)


app.run(debug=True)
