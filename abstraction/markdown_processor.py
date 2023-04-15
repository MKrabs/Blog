import bleach
import markdown


class MarkdownProcessor:

    @classmethod
    def marker(cls, text):
        return markdown.markdown(
            cls.bleacher(text),
            extensions=['tables']
        )

    @classmethod
    def bleacher(cls, text):
        return bleach.clean(
            text,
            tags=['b', 'img', 'iframe'],
            attributes=['class', 'href', 'src', 'style', 'width', 'height']
        )
