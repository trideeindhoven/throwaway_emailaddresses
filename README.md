# throwaway_emailaddresses

This repo makes throwaway emailadresses for your domain. Basically it works like this:

1) You email to makemeanewmailaddress@domain.com. The software will generate a random mailadres and create a forward to the emailadres you are sending with.
2) For x days this mailadres will forward all mail to you. After the x days all email to this random mailadres goes to /dev/null

The system works as follows:
in the virtual table of postfix an entry is created like:
```
*postfix@domain.com  postfix-domain-com
createmeanewemailaddress@domain.com createmeanewemailaddress-domain-com
```
Reload the virtual mailertable:
`makemap /etc/postfix/virtual`

Then create the aliases in /etc/aliases
```
createmeanewemailaddress-domain-com: "|/usr/local/bin/createnewaddress.py"
postfix-domain-com: "|/usr/local/bin/forwardmail.py"
```

Obvisously run 'newaliases' after this.

The result is that all emails get routed to a pythonscript (included in this repository.
createnewaddress.py Generates a new mailaddress (you can choose a prefix and postfix for the generated mailaddresses, this is nice for routing the mailadresses in the virtual mailertable).  
forwardmail.py Reads the sqlite3 database and searches the mailadres where emails needs to be forwarded to. If an entry is older than x days, it gets discarded.
