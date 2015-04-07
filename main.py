__author__ = 'Matjaz'

import os

import simplejson as sj

import goslate


_PHP_PATH = r'path\to\\php.exe'
_Q2A_ROOT = r'path\to\question2answer'


def escape_string(text):
    """Basic string escape function."""

    return text.replace("'", r"\'")

def write(filename, lang_dict, lang='sl'):
    """Write down a definition of a php array with translated text."""
    gs = goslate.Goslate(timeout=2)

    php_code = ["<?php"]
    php_code.append("   /* Some smart comment */")
    php_code.append("   return array(")

    for key in sorted(lang_dict):
        if lang_dict[key] == 'me':
            php_code.append("       '{key}'=>'{value}',".format(key=key, value=_ME_REPLACEMENT))
        elif isinstance(lang_dict[key], str):
            if '^' in lang_dict[key]:
                # -- Insert comment with original string when wildcards are present -- translation breaks them.
                comment = '//{0}'.format(lang_dict[key])
            else:
                comment = ''

            value = gs.translate(lang_dict[key], lang)
            php_code.append("       '{key}'=>'{value}', {comment}".format(key=key, value=escape_string(value),
                                                                          comment=comment))
        else:
            php_code.append("       '{key}'=>'{value}',".format(key=key, value=lang_dict[key]))

    php_code.append("   );")

    f = open(filename, 'wt', encoding='utf-8')
    f.write("\n".join(php_code))
    f.close()


php_exe = _PHP_PATH
php_proxy = r'.\proxy.php'
ref_lang_dir = r'{q2a_root}\qa-include\lang'.format(q2a_root=_Q2A_ROOT)
lang_dir = r'{q2a_root}\qa-lang\sl'.format(q2a_root=_Q2A_ROOT)


if __name__ == '__main__':

    files = os.listdir(ref_lang_dir)
    for file in files:
        if 'emails' in file:
            # -- Emails section translation does not work yet.
            pass
        else:

            print('Translating {file}.'.format(file=file))

            f = os.popen(r'{php_exe} {php_proxy} {lang_dir}\{lang_file}'.format(php_exe=php_exe, php_proxy=php_proxy,
                                                                            lang_dir=ref_lang_dir, lang_file=file))

            data = sj.loads(f.read())
            write(r'{dir}\{file}'.format(dir=lang_dir, file=file), data)

            f.close()