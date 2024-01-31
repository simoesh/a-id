# a-id
Based on the original [Cross-Pollinator BZID](https://hugosimoes.info/blog/2022/02/12/crosspollinator-daily-global-challenge/), [a-id](https://hugosimoes.info/a-id/) is an anonymous cryptographic secure identifier.

An anon-id is composed of two parts: an a-id (public, username, 16 characters) and an h-id (private, password, 32 characters).

Once an anon-id is created
  (python3 a-id.py --create < secret-key.txt)
 the a-id can be displayed and, only together with the h-id, can be validated
  (python3 a-id.py --verify anon-id < secret-key.txt).

As long as the h-id is not compromised, it is virtually impossible to validate an anon-id solely from the public a-id.

This enables each user to build a reputation within a website/app using their provided a-id, with the assurance that these anonymous identifiers are extremely difficult to forge.

One user may use multiple a-ids, but each a-id is used by one user only.
