VERSION = "1.0"

def read_file(filename):
    #with open(filename, encoding='utf8') as file_:
    with open(filename) as file_:
        return file_.read()

def write_to_file(filename, content):
    #with open(filename, 'w', encoding='utf8') as file_:
    with open(filename, 'w') as file_:
        return file_.write(content)


def render_template(template_path, output_path, context):
    content = read_file(template_path)

    for key, value in context.items():
        content = content.replace('{%s}' % key, str(value))

    write_to_file(output_path, content)
