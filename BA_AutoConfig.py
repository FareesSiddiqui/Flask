import flask
import jinja2
import re
import time
from pprint import pprint

app = flask.Flask(__name__, static_url_path="/static")

indexes = {}

# TODO: Make a page for the static config, this way we can change both aspects of the config without clutering the page

# TODO: Fix bug where clicking the static page button twice sends us to a weird path and gives a 404 error the path is static/static/static_config.html when it should be static/static_config.html

def get_vars(template):
    with open(template, "r") as template_file:
        lines = list(template_file.readlines())
    variables = []
    static_vars = []
    static_lines = lines.copy()
    
    for i in range(len(lines)):
        indexes[i] = lines[i]
        matched = re.search(r"############## ------------------->", lines[i])
        
        if matched:
            static_lines.remove(lines[i])
            variables.append(lines[i][:matched.start()-1])

        else:
            static_vars.append(lines[i])
    
    return variables, static_vars

def validate_ip(ip):
    # TODO: check if ip is in correct range
    # TODO: check if ip location is correct (ex, not using a Paris IP for a device in Toronto)
    pass

def generate_html_form(variable_names, file_path, prev_entries):
    html = f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
</head>
<body>

    <section class="hero is-warning">
    <div class="hero-body">
        <center>
            <p class="title">
                BA Auto Config
            </p>
            <p class="subtitle">
                A tool for automatically generating config scripts for devices on the BA network
            </p>
            <a class="button is-link is-responsive is-outlined is-rounded" href="/">Dynamic Config</a>  <a class="button is-link is-responsive is-outlined is-rounded" href="static/static_config.html">Static Config</a>

        </center>
    </div>
    </section>

    <div class="container" style="width: 50%; padding-top: 3vh">
    <form>
    """
    
    for i in range(len(variable_names)):
        label = variable_names[i]
        input_id = variable_names[i]
        html += f"""
        <div class="columns">
            <div class="column is-one-half">
                <label for="{input_id}">{label} </label>
            </div>
            <div class="column">
                <div class="field">
                    <p class="control">
                        <input class="input is-primary" type="text" id="{input_id}" name="{input_id}" value='{prev_entries[i]}'>
                    </p>
                </div>
            </div>
        </div>
        """

    html += """
            <div class="control" style="padding-top: 1vh">
                <button class="button is-link is-light" id="submit_button">Submit</button>
            </div>
        </form>
    </div>
    <script src="static/js/app.js"></script>
</body>
</html>
    """

    with open(file_path, "w") as html_file:
        html_file.write(html)
        
def generate_static_form(variable_names, file_path, prev_entries):
    html = f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
</head>
<body>

    <section class="hero is-warning">
    <div class="hero-body">
        <center>
            <p class="title">
                BA Auto Config
            </p>
            <p class="subtitle">
                A tool for automatically generating config scripts for devices on the BA network
            </p>
            <a class="button is-link is-responsive is-outlined is-rounded" href="/">Dynamic Config</a>  <a class="button is-link is-responsive is-outlined is-rounded" href="static/static_config.html">Static Config</a>

        </center>
    </div>
    </section>

    <div class="container" style="width: 50%; padding-top: 3vh">
    <form>
    """
    
    for i in range(len(variable_names)):
        input_id = variable_names[i]
        html += f"""
        <div class="columns">
            <div class="column">
                <div class="field">
                    <p class="control">
                        <input class="input is-primary" type="text" id="{input_id}" name="{input_id}" value='{prev_entries[i]}'>
                    </p>
                </div>
            </div>
        </div>
        """

    html += """
            <div class="control" style="padding-top: 1vh">
                <button class="button is-link is-light" id="submit_button">Submit</button>
            </div>
        </form>
    </div>
    <script src="static/js/app.js"></script>
</body>
</html>
    """

    with open(file_path, "w") as html_file:
        html_file.write(html)

dynamic_config_variable_names, static_config_vairable_names= get_vars("templates/config_template.txt")
generate_html_form(dynamic_config_variable_names, "templates/index.html", ["" for i in range(len(static_config_vairable_names))])
generate_static_form(static_config_vairable_names, "static/static_config.html", static_config_vairable_names)

time.sleep(0.5)

@app.route("/")
def hello_world():
    return flask.render_template("index.html")

pprint(indexes)

app.run()
