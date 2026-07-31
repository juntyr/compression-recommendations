# Modify the API index page


def on_page_markdown(markdown, page, config, files):
    if page.url.startswith("_ref"):
        markdown = "".join(markdown.splitlines(keepends=True)[1:])

    return markdown
