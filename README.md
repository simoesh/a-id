# f-id
Based on the original [Cross-Pollinator BZID](https://hugosimoes.info/blog/2022/02/12/crosspollinator-daily-global-challenge/), [f-id](https://hugosimoes.info/f-id/) is an anonymous cryptographic secure identifier.

A frag-id is composed of two parts: an f-id (public, 16 characters) and an h-id (private, 32 characters).

Once a frag-id is generated
  (python3 f-id.py --generate < secret_key.txt)
 the f-id can be displayed and, together with the h-id, can be validated
  (python3 f-id.py --verify frag-id < secret_key.txt).

As long as the h-id is not compromised, it is virtually impossible to validate a frag-id solely from the public f-id.

This enables each user to build a reputation within the system using their own f-id, with the assurance that these anonymous identifiers are difficult to forge.

One user may own multiple f-ids, but each f-id is owned by one user only.
