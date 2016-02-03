import json
import urllib


def temperature(q):
    wunderground_response = urllib.urlopen('http://api.wunderground.com/api/ddacf80a930e9c48/conditions/q/%s.json' % urllib.quote(q))
    return json.loads(wunderground_response.read())['current_observation']['temp_f']


def script():
    print 'Where?'
    where = raw_input()
    print 'When?'
    when = raw_input()
    print "It's %s out." % str(temperature(where))


def sub(words, defs):
    output = []
    for word in words:
        if word in defs:
            output.append(defs[word])
        else:
            output.append(word)
    return output

def main():
    defs = {
        'temperature': '34',
    }
    while True:
        try:
            inp = raw_input('> ')
            if inp:
                words = inp.split()
                for word in words:
                    if word in defs:
                        output.append(defs[word])
                    else:
                        output.append(word)
                print ' '.join(output)
        except KeyboardInterrupt:
            print
            continue
        except EOFError:
            break


if __name__ == '__main__':
    script()