# Parse IRCv3 tags
ircv3_tag_escapes = {':': ';', 's': ' ', 'r': '\r', 'n': '\n'}
def _tags_to_dict(tag_list, separator=';'):
    tags = {}
    if separator:
        tag_list = tag_list.split(separator)
    for tag in tag_list:
        tag = tag.split('=', 1)
        if len(tag) == 1:
            tags[tag[0]] = True
        elif len(tag) == 2:
            if '\\' in tag[1]: # Iteration is bad, only do it if required.
                value  = ''
                escape = False
                for char in tag[1]: # TODO: Remove this iteration.
                    if escape:
                        value += ircv3_tag_escapes.get(char, char)
                        escape = False
                    elif char == '\\':
                        escape = True
                    else:
                        value += char
            else:
                value = tag[1] or True
            tags[tag[0]] = value
    print ("TAGS TO DICT OK")

    return tags

# Create the IRCv2/3 parser
def ircv3_message_parser(msg):
    n = msg.split(' ')

    # Process IRCv3 tags
    if n[0].startswith('@'):
        tags = _tags_to_dict(n.pop(0)[1:])
    else:
        tags = {}

    # Process arguments
    if n[0].startswith(':'):
        while len(n) < 2:
            n.append('')
        hostmask = n[0][1:].split('!', 1)
        if len(hostmask) < 2:
            hostmask.append(hostmask[0])
        i = hostmask[1].split('@', 1)
        if len(i) < 2:
            i.append(i[0])
        hostmask = (hostmask[0], i[0], i[1])
        cmd = n[1]
    else:
        cmd = n[0]
        hostmask = (cmd, cmd, cmd)
        n.insert(0, '')

    # Get the command and arguments
    args = []
    c = 1
    for i in n[2:]:
        c += 1
        if i.startswith(':'):
            args.append(' '.join(n[c:]))
            break
        else:
            args.append(i)

    print ("MESSAGE PARSER OK")
    # Return the parsed data
    return cmd, hostmask, tags, args

# Escape tags
def _escape_tag(tag):
    tag = str(tag).replace('\\', '\\\\')
    for i in ircv3_tag_escapes:
        tag = tag.replace(ircv3_tag_escapes[i], '\\' + i)
    print("TAGS ESCAPED")
    return tag

# Convert a dict into an IRCv3 tags string
def _dict_to_tags(tags):
    res = b'@'
    for tag in tags:
        if tags[tag]:
            etag = _escape_tag(tag).replace('=', '-')
            if isinstance(tags[tag], str):
                etag += '=' + _escape_tag(tags[tag])
            etag = (etag + ';').encode('utf-8')
            if len(res) + len(etag) > 4094:
                print("BREAKING - ERROR IN DICT TO TAGS")
                break
            res += etag
    if len(res) < 3:
        return b''
    print("DICT TO TAGS OK")
    return res[:-1] + b' '