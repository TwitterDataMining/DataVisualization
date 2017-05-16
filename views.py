from dataVisualization import app
from models import Example
from forms import LoginForm
from data_process.ProcessData import ProcessData
from flask import render_template, request
import re


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/users', defaults={'offset': 0, 'limit' : 20})
@app.route('/users/<offset>/<limit>')
def user_list(offset, limit):
    pd = ProcessData()
    # offset = int(request.args['offset'])
    # limit = int(request.args['limit'])
    list_of_users = pd.get_users(limit, offset)
    return render_template('users.html', users=list_of_users)

@app.route('/users/<int:id>', methods=['GET', 'POST'])
def user_tweet(id):
    pd = ProcessData()
    user = pd.get_user_tweets(id)
    topics = pd.get_topics()
    topic_words = pd.get_top_words()
    colors = pd.get_colors()
    if request.method == 'GET':
        text = create_html(user)
        return render_template('user_details.html', tweets=text, topics=topics, colors= colors)

    if request.method == 'POST':

        selected = request.form.getlist('selected')
        text = create_html(user, selected, colors, topics, topic_words)
        return render_template('user_details.html', tweets=text, topics=topics, colors=colors)

    return "something went wrong"


def create_html(text, selected=None, colors=None, topics=None, topic_dict= None):
    ts = [line['tweets'] for line in text]
    text = " ".join(ts)
    if selected is None:
        return text
    for idx, topic in enumerate(selected):
        color = colors[idx]
        bac = colors[idx + 1]
        words = topic_dict[topic.strip()];
        regex = re.compile(r'\b(?:%s)\b' % '|'.join(words))
        i = 0; output = ""
        for m in regex.finditer(text):
            output += "".join([text[i:m.start()],
                               "<strong><span style='color:{0}; background-color:{1}'>".format(color, bac),
                               text[m.start():m.end()],
                               "<span></strong>"])
            i = m.end()
        text = output
    return text






@app.route('/create_db')
def create_data():
    pd = ProcessData()
    pd.create_data()
    return "Done"