import flask
import jinja2
import re
import time

app = flask.Flask(__name__)

# TODO: Make a page for the static config, this way we can change both aspects of the config without clutering the page


def get_vars(template):
    with open(template, "r") as template_file:
        lines = list(template_file.readlines())
    variables = []
    for i in range(len(lines)):
        matched = re.search(r"############## ------------------->", lines[i])
        
        if matched:
            variables.append(lines[i][:matched.start()-1])
    
    return variables

def validate_ip(ip):
    # TODO: check if ip is in correct range
    # TODO: check if ip location is correct (ex, not using a Paris IP for a device in Toronto)
    pass

def generate_html_form(variable_names):
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
        </center>
    </div>
    </section>

    <div class="container" style="width: 50%; padding-top: 3vh">
    <form>
    """
    
    for variable_name in variable_names:
        label = variable_name
        input_id = variable_name
        html += f"""
        <div class="columns">
            <div class="column is-one-half">
                <label for="{input_id}">{label}: </label>
            </div>
            <div class="column">
                <div class="field">
                    <p class="control">
                        <input class="input is-primary" type="text" id="{input_id}" name="{input_id}">
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
</body>
</html>
    """

    with open("templates/index.html", "w") as html_file:
        html_file.write(html)

variable_names = get_vars("templates/config_template.txt")
generate_html_form(variable_names)
print(variable_names)

time.sleep(0.5)

@app.route("/")
def hello_world():
    return flask.render_template("index.html")

app.run(debug=True)