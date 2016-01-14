from flask import Flask
from flask import request
from flask import jsonify
import json
import subprocess

app = Flask(__name__)
config = None

@app.route("/", methods=['POST'])
def hook_listen():
    if request.method == 'POST':
        token = request.args.get('token')
        if token == config['token']:
            hook = request.args.get('hook')
            if hook:
                hook_value = config['hooks'].get(hook)
                if hook_value:
                    s = request.data
                    data = json.loads(s)
                    print "Push date: {data}".format(data=data['push_data']['pushed_at'])
                    print "Push images: {data}".format(data=data['push_data']['images'])
                    print "Push tag: {data}".format(data=data['push_data']['tag'])
                    print "Repo url: {data}".format(data=data['repository']['repo_url'])
                    print "Repo visibility: {data}".format(data=data['repository']['is_private'])
                    print "Repo name: {data}".format(data=data['repository']['repo_name'])
                    print "Repo status: {data}".format(data=data['repository']['status'])
                    try:
#                        subprocess.call([hook_value, pretty_request])
#                        subprocess.call([hook_value, pretty_request])
                        subprocess.call(['scripts/testing.sh',
                            '--push_date', '{data}'.format(data=data['push_data']['pushed_at']),
                            '--tag', '{data}'.format(data=data['push_data']['tag']),
                            '--repo_name', '{data}'.format(data=data['repository']['repo_name'])])
                        subprocess.call([hook_value, data])
                        return jsonify(success=True), 200
                    except OSError as e:
                        return jsonify(success=False, error=str(e)), 400
                else:
                    return jsonify(success=False, error="Hook not found"), 404
            else:
                return jsonify(success=False, error="Invalid request: missing hook"), 400
        else:
            return jsonify(success=False, error="Invalid token"), 400

def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

if __name__ == "__main__":
    config = load_config()
    app.run(host=config.get('host', 'localhost'), port=config.get('port', 8000))
