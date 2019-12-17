
def attached_comment(parser, start_line):
    comment = "No attached comments."

    if start_line < 0:
        return comment

    previous_line = parser.content.split('\n')[start_line - 1]

    if previous_line.find('*/') >= 0 or previous_line.find('//') >= 0:
        comment = parser.comments[-1]
        parser.comments_attached[-1] = True

    return comment
