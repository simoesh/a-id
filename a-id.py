# Copyright 2024 Hugo Simoes <hugosimoes@hugosimoes.info>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sys import stdin, stdout, stderr

from hashlib import sha3_256

RANDOM_BYTES_DIV_3 = 8 # 192 random bits
hexachars = "bcdfghjklprstvxz"
b64chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-"

def create(secret_key):
    from os import urandom
    h_id = ""
    bits = urandom(3*RANDOM_BYTES_DIV_3)
    for j in range(int(RANDOM_BYTES_DIV_3)):
        i0 = bits[j*3+0]&0x3f
        i1 = ((bits[j*3+1]&0x0f)<<2)+((bits[j*3+0]&0xc0)>>6)
        i2 = ((bits[j*3+2]&0x03)<<4)+((bits[j*3+1]&0xf0)>>4)
        i3 = (bits[j*3+2]&0xfc)>>2
        c0 = b64chars[i0]
        c1 = b64chars[i1]
        c2 = b64chars[i2]
        c3 = b64chars[i3]
        h_id += f"{c0}{c1}{c2}{c3}"
    secret_key = secret_key.encode('utf-8')
    x4_a_id = sha3_256(secret_key+bits+secret_key).digest()
    a_id = ""
    for j in range(int(len(x4_a_id)/4)):
        b = (x4_a_id[j*4+0]^x4_a_id[j*4+1]^x4_a_id[j*4+2]^x4_a_id[j*4+3])
        a_id += hexachars[(b&0xf0)>>4]+hexachars[b&0x0f]
    return f"{a_id}{h_id}"

def verify(secret_key, anon_id):
    from struct import pack
    if len(anon_id) != 16+RANDOM_BYTES_DIV_3*4: return False
    v_id = anon_id[0:16]
    h_id = anon_id[16:]
    bits = b""
    for j in range(int(len(h_id)/4)):
        c0 = h_id[j*4+0]
        c1 = h_id[j*4+1]
        c2 = h_id[j*4+2]
        c3 = h_id[j*4+3]
        try:
            i0 = b64chars.index(c0)
            i1 = b64chars.index(c1)
            i2 = b64chars.index(c2)
            i3 = b64chars.index(c3)
        except ValueError:
            return False
        b0 = ((i1&0x03)<<6)+((i0&0x3f)>>0)
        b1 = ((i2&0x0f)<<4)+((i1&0x3c)>>2)
        b2 = ((i3&0x3f)<<2)+((i2&0x30)>>4)
        bits += pack("BBB", b0, b1, b2)
    secret_key = secret_key.encode('utf-8')
    x4_a_id = sha3_256(secret_key+bits+secret_key).digest()
    a_id = ""
    for j in range(int(len(x4_a_id)/4)):
        b = (x4_a_id[j*4+0]^x4_a_id[j*4+1]^x4_a_id[j*4+2]^x4_a_id[j*4+3])
        a_id += hexachars[(b&0xf0)>>4]+hexachars[b&0x0f]
    return (v_id == a_id)

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2 and argv[1] == "--create":
        print(create(stdin.readline().rstrip()), file=stdout)
    elif len(argv) == 3 and argv[1] == "--verify":
        print("ok" if verify(stdin.readline().rstrip(), argv[2]) else "ko",
              file=stdout)
    else:
        print(f"Usage: python3 {argv[0]} "+
              "--create < secret-key.txt", file=stderr)
        print(f"   or: python3 {argv[0]} "+
              "--verify anon-id < secret-key.txt", file=stderr)
