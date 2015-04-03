__author__ = 'Matjaz'

import os

import simplejson as sj

import goslate

_PHP_PATH = r'\path\to\php.exe'
_Q2A_ROOT = r'\path\to\q2a\root'

def escape_string(text):
    """Basic string escape function."""

    return text.replace("'", r"\'")

def write(filename, lang_dict, lang='sl'):
    """Write down a definition of a php array with translated text."""
    gs = goslate.Goslate()

    php_code = ["<?php"]
    php_code.append("   /* Some smart comment */")
    php_code.append("   return array(")

    for key in sorted(lang_dict):
        value = gs.translate(lang_dict[key], lang)
        php_code.append("       '{key}'=>'{value}',".format(key=key, value=escape_string(value)))

    php_code.append("   );")

    f = open(filename, 'wt', encoding='utf-8')
    f.write("\n".join(php_code))
    f.close()


php_exe = _PHP_PATH
php_proxy = r'.\proxy.php'
ref_lang_dir = r'{q2a_root}\qa-include\lang'.format(q2a_root=_Q2A_ROOT)
lang_dir = r'{q2a_root}\qa-lang\sl'.format(q2a_root=_Q2A_ROOT)

if __name__ == '__main__':
    fname = 'qa-lang-admin.php'

    f = os.popen(r'{php_exe} {php_proxy} {lang_dir}\{lang_file}'.format(php_exe=php_exe, php_proxy=php_proxy,
                                                                    lang_dir=lang_dir, lang_file=fname))

    data = sj.loads(f.read())

    write(fname, data)