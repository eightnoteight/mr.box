import requests
import re
from flask import Flask, jsonify, render_template
app = Flask(__name__)

USER_PAGE = 'http://www.spoj.com/users/{username}/'

def getSolvedProblems(doc, username):
    pattern = '/status/(.{3,8}),' + username + '/'
    return re.findall(pattern, doc)

@app.route('/spojscrap/userdiff/<username1>/<username2>/')
def userdiff(username1, username2):
    u1solved = getSolvedProblems(
        requests.get(USER_PAGE.format(username=username1)).content, username1)
    u2solved = getSolvedProblems(
        requests.get(USER_PAGE.format(username=username2)).content, username2)
    return jsonify(**{
        username1: u1solved,
        username2: u2solved,
        username1 + '-' + username2: list(set(u1solved) - set(u2solved)),
        username2 + '-' + username1: list(set(u2solved) - set(u1solved))
    })
    # print 'solved by {} but not by {}'.format(username1, username2)
    # print '\n'.join('    {: >4}.{}'.format(i, prob) for i, prob in enumerate(
    #     set(u1solved) - set(u2solved)))
    # print 'solved by {} but not by {}'.format(username2, username1)
    # print '\n'.join('    {: >4}.{}'.format(i, prob) for i, prob in enumerate(
    #     set(u2solved) - set(u1solved)))


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
