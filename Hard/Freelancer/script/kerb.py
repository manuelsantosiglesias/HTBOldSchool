#!/usr/bin/env python3
##############################################################################
#
#   Lee el archivo ccache que tenemos y nos muestra la info del ticket
#
##############################################################################

'''
Based on https://gist.github.com/cluther/6538887#file-krb5_ccache-py
'''

from base64 import b64encode
from datetime import datetime
from struct import unpack
import optparse
import os
import tempfile

class CCache(object):
    def __init__(self, data):
        self.size = len(data)
        print(f"Total size of data: {self.size}")
        idx = 0
        if self.size < 4:
            raise ValueError("Not enough data to read file format version and header length.")
        self.file_format_version, self.headerlen = unpack(
            '!HH', data[idx:idx+4])
        print(f"File format version: {self.file_format_version}, Header length: {self.headerlen}")
        idx += 4
        headers_idx = idx

        self.headers = []
        while idx < headers_idx + self.headerlen:
            if idx + self.headerlen > self.size:
                raise ValueError("Not enough data to read headers.")
            header = Header(data[idx:idx+self.headerlen])
            idx += header.size
            self.headers.append(header)

        print(f"Data after headers: {idx}")
        
        # Add primary_principal.
        if idx + 8 > self.size:
            raise ValueError("Not enough data to read primary principal.")
        self.primary_principal = Principal(data[idx:])
        idx += self.primary_principal.size

        print(f"Data after primary principal: {idx}")
        
        # Add credentials.
        self.credentials = []
        while idx < self.size:
            credential = Credential(data[idx:])
            idx += credential.size
            self.credentials.append(credential)

        print(f"Data after credentials: {idx}")

    def __str__(self):
        return (
            "File format version: {}\n"
            "Header length: {}\n"
            "Headers:\n{}\n"
            "Primary Principal:\n{}\n"
            "Credentials:\n{}\n".format(
                self.file_format_version,
                self.headerlen,
                '\n'.join(map(str, self.headers)),
                str(self.primary_principal),
                '\n'.join(map(str, self.credentials))))


class Header(object):
    tag = None                  # uint16 (H,2)
    taglen = None               # uint16 (H,2)
    tagdata = None              # uint8[] | DeltaTime

    size = None

    def __init__(self, data):
        self.size = 0

        if len(data) < 4:
            raise ValueError("Not enough data to read header tag and tag length.")
        self.tag, self.taglen = unpack('!HH', data[:4])

        if self.tag == 1:
            if len(data) < 4 + self.taglen:
                raise ValueError("Not enough data to read DeltaTime.")
            self.tagdata = DeltaTime(data[4:4+self.taglen])
        else:
            if len(data) < 4 + self.taglen:
                raise ValueError("Not enough data to read tagdata.")
            self.tagdata = unpack('!{}c'.format(self.taglen), data[4:4+self.taglen])

        self.size = 4 + self.taglen

    def __str__(self):
        return (
            "  Tag: {}\n"
            "  Tag length: {}\n"
            "  Tag data: {}\n".format(
                self.tag,
                self.taglen,
                str(self.tagdata)))


class DeltaTime(object):
    time_offset = None          # uint32 (I,4)
    usec_offset = None          # uint32 (I,4)

    size = None

    def __init__(self, data):
        if len(data) < 8:
            raise ValueError("Not enough data to read DeltaTime.")
        self.time_offset, self.usec_offset = unpack('!II', data)
        self.size = len(data)

    def __str__(self):
        return "DeltaTime (time_offset:{}, usec_offset:{})".format(
            self.time_offset, self.usec_offset)


class Credential(object):
    client = None               # Principal
    server = None               # Principal
    key = None                  # KeyBlock
    time = None                 # Times
    is_skey = None              # uint8 (B,1)
    tktflags = None             # uint32 (I,4)
    num_address = None          # uint32 (I,4)
    addrs = None                # Address[]
    num_authdata = None         # uint32 (I,4)
    authdata = None             # AuthData[]
    ticket = None               # CountedOctetString
    second_ticket = None        # CountedOctetString

    size = None

    def __init__(self, data):
        self.client = Principal(data)
        idx = self.client.size

        self.server = Principal(data[idx:])
        idx += self.server.size

        self.key = KeyBlock(data[idx:])
        idx += self.key.size

        self.time = Times(data[idx:])
        idx += self.time.size

        if idx + 9 > len(data):
            raise ValueError("Not enough data to read credential header.")
        self.is_skey, self.tktflags, self.num_address = unpack(
            '!BII', data[idx:idx+9])

        idx += 9

        self.addrs = []
        while len(self.addrs) < self.num_address:
            if idx >= len(data):
                raise ValueError("Not enough data to read addresses.")
            address = Address(data[idx:])
            self.addrs.append(address)
            idx += address.size

        if idx + 4 > len(data):
            raise ValueError("Not enough data to read auth data count.")
        self.num_authdata, = unpack('!I', data[idx:idx+4])
        idx += 4

        self.authdata = []
        while len(self.authdata) < self.num_authdata:
            if idx >= len(data):
                raise ValueError("Not enough data to read auth data.")
            authdata = AuthData(data[idx:])
            self.authdata.append(authdata)
            idx += authdata.size

        if idx >= len(data):
            raise ValueError("Not enough data to read ticket.")
        self.ticket = Ticket(data[idx:])
        idx += self.ticket.size

        if idx >= len(data):
            raise ValueError("Not enough data to read second ticket.")
        self.second_ticket = Ticket(data[idx:])
        idx += self.second_ticket.size

        self.size = idx

    def __str__(self):
        return (
            "  Client: {}\n"
            "  Server: {}\n"
            "  Key: {}\n"
            "  Times:\n{}\n"
            "  SKey: {}\n"
            "  Ticket flags: {}\n"
            "  Addresses: {}\n"
            "  Auth data: {}\n"
            "  Ticket: {}\n\n"
            "  Second ticket: {}\n\n".format(
                str(self.client),
                str(self.server),
                str(self.key),
                str(self.time),
                'Yes' if self.is_skey else 'No',
                self.tktflags,
                str(self.addrs),
                str(self.authdata),
                str(self.ticket),
                str(self.second_ticket)))



class KeyBlock(object):
    keytype = None              # uint16 (H,2)
    etype = None                # uint16 (H,2)
    keylen = None               # uint16 (H,2)
    keyvalue = None             # uint8[]

    size = None

    def __init__(self, data):
        if len(data) < 6:
            raise ValueError("Not enough data to read KeyBlock.")
        self.keytype, self.etype, self.keylen = unpack('!HHH', data[:6])
        if len(data) < 6 + self.keylen:
            raise ValueError("Not enough data to read key value.")
        self.keyvalue = data[6:6+self.keylen]
        self.size = 6 + self.keylen

    def __str__(self):
        return b64encode(self.keyvalue).decode('utf-8')


class Times(object):
    authtime = None             # uint32 (I,4)
    starttime = None            # uint32 (I,4)
    endtime = None              # uint32 (I,4)
    renew_till = None           # uint32 (I,4)

    size = None

    def __init__(self, data):
        if len(data) < 16:
            raise ValueError("Not enough data to read Times.")
        self.authtime, self.starttime, self.endtime, self.renew_till = unpack(
            '!IIII', data[:16])
        self.size = 16

    def __str__(self):
        return (
            "    Auth: {}\n"
            "    Start: {}\n"
            "    End: {}\n"
            "    Renew till: {}\n".format(
                datetime.fromtimestamp(self.authtime).isoformat(),
                datetime.fromtimestamp(self.starttime).isoformat(),
                datetime.fromtimestamp(self.endtime).isoformat(),
                datetime.fromtimestamp(self.renew_till).isoformat()))


class Address(object):
    addrtype = None             # uint16 (H,2)
    addrdata = None             # CountedOctetString

    size = None

    def __init__(self, data):
        if len(data) < 2:
            raise ValueError("Not enough data to read Address.")
        self.addrtype, = unpack('!H', data[:2])
        self.addrdata = CountedOctetString(data[2:])
        self.size = 2 + self.addrdata.size


class AuthData(object):
    authtype = None             # uint16 (H,2)
    authdata = None             # CountedOctetString

    size = None

    def __init__(self, data):
        if len(data) < 2:
            raise ValueError("Not enough data to read AuthData.")
        self.authtype, = unpack('!H', data[:2])
        self.authdata = CountedOctetString(data[2:])
        self.size = 2 + self.authdata.size


class Principal(object):
    def __init__(self, data):
        if len(data) < 8:
            raise ValueError("Not enough data to read Principal.")
        self.name_type, self.num_components = unpack('!II', data[:8])
        idx = 8

        self.realm = CountedOctetString(data[idx:])
        idx += self.realm.size

        self.components = []
        while len(self.components) < self.num_components:
            if idx >= len(data):
                raise ValueError("Not enough data to read components.")
            component = CountedOctetString(data[idx:])
            self.components.append(component)
            idx += component.size

        self.size = idx

    def __str__(self):
        return (
            "    Name type: {}\n"
            "    Realm: {}\n"
            "    Components: {}\n".format(
                self.name_type,
                str(self.realm),
                str(self.components)))

class CountedOctetString(object):
    length = None               # uint32 (I, 4)
    data = None                 # uint8[]

    size = None

    def __init__(self, data):
        if len(data) < 4:
            raise ValueError("Not enough data to read CountedOctetString length.")
        self.length, = unpack('!I', data[:4])
        if len(data) < 4 + self.length:
            raise ValueError("Not enough data to read CountedOctetString data.")
        self.data = data[4:4+self.length]
        self.size = 4 + self.length

    def __str__(self):
        return b64encode(self.data).decode('utf-8')


class Ticket(CountedOctetString):
    pass


def main():
    parser = optparse.OptionParser(usage="Usage: %prog [options] <ccache file>")
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        exit(1)

    filename = args[0]
    if not os.path.isfile(filename):
        print(f"{filename} is not a valid file.")
        exit(1)

    with open(filename, 'rb') as f:
        data = f.read()

    try:
        ccache = CCache(data)
        print(ccache)
    except ValueError as e:
        print(f"Error parsing ccache file: {e}")

if __name__ == "__main__":
    main()
