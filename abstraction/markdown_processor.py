import bleach
import markdown


class MarkdownProcessor:
    def __init__(self, text):
        self.text = text

    def marker(self, text):
        return markdown.markdown(
            self.bleacher(text),
            extensions=['tables']
        )

    @staticmethod
    def bleacher(text):
        return bleach.clean(
            text,
            tags=['b', 'img', 'iframe'],
            attributes=['class', 'href', 'src', 'style', 'width', 'height']
        )
