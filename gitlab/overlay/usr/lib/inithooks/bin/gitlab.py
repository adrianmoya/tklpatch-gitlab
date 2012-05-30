#!/usr/bin/python
"""Set Gitlab admin password and email

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively

"""

import sys
import getopt
from passlib.hash import bcrypt

from dialog_wrapper import Dialog
from mysqlconf import MySQL

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "Gitlab Password",
            "Enter new password for the Gitlab 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "Gitlab Email",
            "Enter email address for the Gitlab 'admin' account.",
            "admin@example.com")
    
    hashpass = bcrypt.encrypt(password, rounds=10)

    m = MySQL()
    m.execute('UPDATE gitlab.users SET email=\"%s\" WHERE name=\"Administrator\";' % email)
    m.execute('UPDATE gitlab.users SET encrypted_password=\"%s\" WHERE name=\"Administrator\";' % hashpass)

if __name__ == "__main__":
    main()
