import flask
import jinja2
import re
import time

app = flask.Flask(__name__)


def get_var_name(template):
    variable_pattern = r'{{\s*([A-Za-z_][A-Za-z0-9_]*)\s*}}'
    variable_names = re.findall(variable_pattern, template)
    return variable_names

def parse_template(file_path):
    with open(file_path, 'r') as template_file:
        template_content = template_file.read()
    return get_var_name(template_content)

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

    <div class="container" style="width: 20%;">
    <form>
    """
    
    for variable_name in variable_names:
        label = variable_name.capitalize()
        input_id = variable_name
        html += f"""
        <div class="field">
            <label for="{input_id}">{label}:</label>
            <input class="input is-primary" type="text" size="10" id="{input_id}" name="{input_id}">
        </div>
        """

    html += """
            <div class="control" style="padding-top: 1vh">
                <button class="button is-link is-light">Submit</button>
            </div>
        </form>
    </div>
</body>
</html>
    """

    with open("templates/index.html", "w") as html_file:
        html_file.write(html)

variable_names = parse_template('templates/config_template.txt')
generate_html_form(variable_names)
print(variable_names)

time.sleep(0.5)

@app.route("/")
def hello_world():
    return flask.render_template("index.html")

app.run(debug=True)